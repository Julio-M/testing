# importing modules
import os
import shutil
import subprocess
import git
import uuid
from pathlib import Path
import glob
import shutil

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Helper methods for refactoring
def color_words(color,word):
     print(color+word+bcolors.ENDC)

def replace_words_in_files(destination_dir,word_to_replace,new_word):
    newfiles=os.listdir(destination_dir)
    for filepath in glob.iglob(f'{destination_dir}/**/*.*', recursive=True):
        with open(filepath) as file:
            s = file.read()
            s = s.replace(word_to_replace, f'{new_word}')
        with open(filepath, "w") as file:
            file.write(s)

def copy_files_from_folder():
    return

def replace_words_in_one_file(filepath,word_to_replace,new_word):
    with open(filepath) as file:
        s = file.read()
        s = s.replace(word_to_replace, f'{new_word}')
    with open(filepath, "w") as file:
        file.write(s)

# check whether the specified repositories exist
def check_for_repos(path,repositories,ssh_prefix):
    if not os.path.exists(path):
        color_words(bcolors.BOLD ,'Creating temporary directory')
        os.mkdir(path)
        color_words(bcolors.BOLD ,'Directory created')
    
    # Check whether the specified path exists or not
    for repo in repositories:
        isExist = os.path.exists(f'{path}/{repo}')
        if isExist:
            print('Repository' + f' {bcolors.OKBLUE}{repo}{bcolors.ENDC} ' + 'exists locally')
        else:
            print('Repository' + f' {bcolors.WARNING}{repo}{bcolors.ENDC} ' + 'does not exist locally')
            print('Fetching from github.....')
            try:
                repo = git.Repo.clone_from(f"{ssh_prefix}/{repo}.git", f"{path}/{repo}")
                # subprocess.run(["git","-C",f"{path}", "clone", f"{ssh_prefix}/{repo}.git"])
                print(repo)
            except git.exc.GitCommandError as e:
                color_words(bcolors.FAIL,str(e))

# Checking for staging branch under new service repo and create it if it doesn't exist
def check_for_staging_branch_service(path,service_name):
    color_words(bcolors.OKBLUE ,'Checking for staging branch under new service repo')
    try:
        service_repo = git.Repo(os.path.join(f"{path}/{service_name}"))
        branches = service_repo.references
        if "origin/staging" in branches or "staging" in branches:
            color_words(bcolors.BOLD ,'Branch staging exists')
        else:
            color_words(bcolors.WARNING ,'Branch staging does not exist')
            color_words(bcolors.BOLD ,f'Creating new branch "staging" in {service_repo}')
            service_repo.git.checkout('-b', 'staging')
    except OSError as e:
        color_words(bcolors.UNDERLINE ,'Have you checked if the service repository exists?')

# Add service repo name to create an ecr repository for the new service
def add_input_to_existing_file(path,service_name):
    enviroments = ["staging/global/ecr","global/iam"]
    for env in enviroments:
        try:
            file_path = f"{path}/infra-terrafrom/environments/{env}/inputs.hcl"
            new_service = f'   "{service_name}"\n'
            with open(file_path,"r") as f:
                data = f.readlines()
                if f'   "{service_name}",\n' in data or new_service in data:
                    color_words(bcolors.BOLD ,f'{service_name} exists in {env}')
                else:
                    print('DATA',data[-3][:-1])
                    data[-3] = data[-3][:-1] + ",\n"
                    data.insert(-2,new_service)
                    # and write everything back
                    color_words(bcolors.BOLD ,f'Editing file: {f.name}')
                    with open(file_path, 'w') as file:
                        file.writelines(data)
                    subprocess.run(["cat",f"{file_path}"])
        except:
            color_words(bcolors.FAIL ,f'Failed to write. Does {file_path} exist?')

# Add container image build and publish pipeline
def add_container_image_build(path,service_name):
    work_path = f'{path}/{service_name}/.github/workflows'
    try:
        os.makedirs(work_path)
        print("Directory '%s' created successfully" %work_path)
    except OSError as error:
        print(error)
        print("Directory '%s' can not be created" %work_path)
    # Path(f'{work_path}/build-and-push-image.yaml').touch()
    f = open(f'{work_path}/build-and-push-image.yaml', "a")
    f.write(f'''name: Build and Push Container Image to ECR

on: 
  push:
    branches:
      - staging
      - production

jobs:
  build-and-push:
    runs-on: self-hosted

    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v2     

      - name: Build and Push
        uses: amun/infra-shared-workflows/build-and-push-image@main
        with:
          aws_account_id: "764933035250"
          region: us-east-2
          repo: "{service_name}-${{ github.base_ref || github.ref_name }}"
          build_context: .
          dockerfile_path: "./Dockerfile"
''')

# Add a new service account role
def add_service_account(path,service_name):
    serv_under = service_name.replace("-","_")
    work_path = f'{path}/infra-terrafrom/modules/eks-serviceaccounts'
    f = open(f'{work_path}/{service_name}_role.tf', "a")
    f.write(f'''module "{serv_under}_role" {{
    source      = "cloudposse/eks-iam-role/aws"
    version     = ">= 0.11.1"

    aws_account_number          = data.aws_caller_identity.current.account_id
    eks_cluster_oidc_issuer_url = var.cluster_oidc_issuer_url

    # Create a role for the service account named `{serv_under}` in the Kubernetes namespace `{serv_under}`
    service_account_name      = "${{var.environment_code}}-${{var.resource_region}}-{service_name}-sa"
    service_account_namespace = "{service_name}"
    # JSON IAM policy document to assign to the service account role
    aws_iam_policy_document   = [data.aws_iam_policy_document.{serv_under}.json]
    }}

    data "aws_iam_policy_document" "{serv_under}" {{
    statement {{
        sid = "AllowAllOnS3Objects"

        actions = [
        "s3:*"
        ]

        effect    = "Allow"
        resources = ["*"]
    }}
    }}''')
    color_words(bcolors.BOLD ,f'You see the file here: {work_path}/{service_name}_role.tf')

def create_helm_chart(path,service_name):
    work_path = f'{path}/infra-charts/{service_name}'
    try:
        # path to source directory
        src_dir = f'{path}/infra-charts/lima-cms'
        # path to destination directory
        dest_dir = work_path
        ## getting all the files in the source directory
        files = os.listdir(src_dir)
        shutil.copytree(src_dir, dest_dir)
        print("Directory '%s' created successfully" %work_path)
        replace_words_in_files(dest_dir,'lima-cms',service_name)
        color_words(bcolors.BOLD ,f'You see the helm-chart files here: {dest_dir}')
    except OSError as error:
        print(error)
        print("Directory '%s' can not be created" %work_path)

def create_apps_base_helm_release(path,service_name):
    work_path = f'{path}/infra-gitops/apps/base/{service_name}'
    work_path2 = f'{path}/infra-gitops/sources/image-repos/{service_name}.yaml'
    work_path3 = f'{path}/infra-gitops/sources'
    src_dir = f'{path}/infra-gitops/'
    try:
        src_dir1 = f'{src_dir}/apps/base/lima-cms'
        dest_dir1 = work_path
        shutil.copytree(src_dir1, dest_dir1)
        print("Directory '%s' created successfully" %work_path)
        replace_words_in_files(dest_dir1,'lima-cms',service_name)
    except OSError as error:
        print(error)
        print("Directory '%s' can not be created" %work_path)
    try:
        src_dir2= f'{src_dir}/sources/image-repos/lima-cms.yaml'
        dest_dir2 = work_path2
        shutil.copy(src_dir2, dest_dir2)
        replace_words_in_one_file(dest_dir2,"lima-cms",service_name)
    except OSError as error:
        print(error)
        print("Directory '%s' can not be created" %work_path2)

# # Add, commit, and push to ticket branch
# def push_to_new_ticket_branch():
#     try:

#     except:


# You can choose to delete the directory that holds all the repos (maybe)?
def delete_all(path):
    answer=input('Do you want to delete the temp directory? (Yy/Nn): ')

    if answer=='Y' or answer=='y':
        color_words(bcolors.BOLD ,'Deleting directory....')
        try:
            shutil.rmtree(path)
            color_words(bcolors.BOLD ,'Directory deleted!')
        except OSError as e:
            print("Error: %s : %s" % (path, e.strerror))
    else:
        color_words(bcolors.BOLD ,f'You can find the directory here: {path}')

if __name__ == "__main__":
    # Service name
    service_name = input('Service name: ')

    # Github repository
    github_repo = input(f'Github repo for service [{service_name}]: ') or service_name

    # Ticket
    ticket_number = input(f'Ticket number [tn- (random id)]: ') or f'tn-{uuid.uuid4().hex[:4]}'

    # Branch name (keep it to 3 letters)
    valid=False
    while not valid:
        branch_n = input(f'Branch name (3 letters): ')
        if len(branch_n)%3==0:
            valid=True
        else:
            color_words(bcolors.WARNING,'Branch name must be 3 letters')
    
    branch_name = ticket_number + "-" + branch_n

    print(branch_name)
    # SSH prefix
    ssh_prefix = 'git@github.com:amun'
    # List of repositories needed for the service
    repositories = [service_name,'infra-terrafrom','infra-charts']

    # Specify path
    path = os.path.expanduser('~/Documents/code')

    check_for_repos(path,repositories,ssh_prefix)
    check_for_staging_branch_service(path,service_name)
    add_input_to_existing_file(path,service_name)
    add_container_image_build(path,service_name)
    add_service_account(path,service_name)
    create_helm_chart(path,service_name)
    create_apps_base_helm_release(path,service_name)
    delete_all(path)