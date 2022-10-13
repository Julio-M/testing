# Create ECR Repo

# Check if repository exists
# ```
# ~$ git ls-remote <existing_repo> -q
# ~$ echo $?
# 0
#```

# importing modules
import os
import shutil
import subprocess

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
            subprocess.run(["git","-C",f"{path}", "clone", f"{ssh_prefix}/{repo}.git"])

def check_for_staging_branch_service():
    print('BRANCHES' + 'does not exist locally')
    cmd = [ 'if','[git branch --list $hello]','then','echo','Branch name $branch_name already exists.','fi' ]
    subprocess.run( cmd )

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
    # check_for_staging_branch_service()
    delete_all(path)