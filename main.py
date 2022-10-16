# Create ECR Repo

# importing modules
import os
import shutil
import subprocess
import git

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

def color_words(color,word):
     print(color+word+bcolors.ENDC)

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
    try:
        file_path = f"{path}/reddit-scrape/inputs.hcl"
        new_service = f'        "{service_name}"\n'
        with open(file_path,"r") as f:
            data = f.readlines()
            if f'        "{service_name}",\n' in data:
                color_words(bcolors.BOLD ,f'{service_name} ECR repository exists')
                return 
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


# You can choose to delete the directory that holds all the repos (maybe)?
def delete_all(path):
    answer=input('Do you want to delete the temp directory? (Yy/Nn): ')

    if answer=='Y' or answer=='y':
        color_words(bcolors.BOLD ,'Deleting directory....')
        try:
            shutil.rmtree(path)
            color_words(bcolors.BOLD ,'Deleting deleted!')
        except OSError as e:
            print("Error: %s : %s" % (path, e.strerror))
    else:
        color_words(bcolors.BOLD ,f'You can find the directory here: {path}')

if __name__ == "__main__":
    # Service name
    service_name = input('Service name: ')

    # SSH prefix
    ssh_prefix = 'git@github.com:Julio-M'
    # List of repositories needed for the service
    repositories = [service_name,'testing', 'firstscript', 'web-scrape']

    # Specify path
    path = os.path.expanduser('~/Documents/code')

    check_for_repos(path,repositories,ssh_prefix)
    check_for_staging_branch_service(path,service_name)
    add_input_to_existing_file(path,service_name)
    delete_all(path)