# Assumption is you have done this:
# Warning: Make sure this virtualenv is different from the env_build, so it doesn't pull unnecessary dependencies
# virtualenv --python=/usr/bin/python3 env_build
# source env_build/bin/activate
# pip install PyQT5 pyinstaller

import os
import shutil
from time import sleep
import platform
import subprocess

from git import Repo


SL_REPO_DIR = os.path.join(os.getcwd(), "spring-launcher")
SL_REPO_URL = "https://github.com/Spring-Chobby/spring-launcher"

SL_DIST_REPO_DIR = os.path.join(os.getcwd(), "spring-launcher-dist")
SL_DIST_REPO_URL = "git@github.com:Spring-Chobby/spring-launcher-dist.git"

platformToDir = {
    "Linux": "linux",
    "Darwin": "mac",
    "Windows": "windows"
}

commitSHA = None

def do_freeze():
    if os.name == 'posix':
        output = subprocess.run("bash freeze.sh", cwd=os.getcwd(), shell=True)
    elif os.name == 'nt':
        output = subprocess.run("freeze.bat", cwd=os.getcwd(), shell=True)
    else:
        print("Weird OS? {}".format(os.name))

def upload_freeze(distDir):
    print("First making sure we have the latest version...")
    repoDist.git.reset('--hard')
    repoDist.remotes.origin.pull(rebase=True)
    distDirPath = os.path.join(SL_DIST_REPO_DIR, distDir)
    if os.path.exists(distDirPath):
        shutil.rmtree(distDirPath)
    shutil.copytree(os.path.join(SL_REPO_DIR, "spring_launcher/dist/launcher"),
                    distDirPath)
    print("Commiting and pushing the latest version")
    repoDist.git.add(A=True)
    repoDist.git.commit('-m', 'Sync {}: {}'.format(commitSHA, distDir), author='{}-bot <>'.format(distDir))
    repoDist.remotes.origin.push()
    print("Pushed.")


initialFreeze = False
if not os.path.exists(SL_REPO_DIR):
    repo = Repo.clone_from(SL_REPO_URL, SL_REPO_DIR)
    print("Initialized repository: {}.".format(SL_REPO_DIR))
    initialFreeze = True 
else:
    repo = Repo(SL_REPO_DIR)
    print("Loaded existing repository: {}.".format(SL_REPO_DIR))

if not os.path.exists(SL_DIST_REPO_DIR):
    repoDist = Repo.clone_from(SL_DIST_REPO_URL, SL_DIST_REPO_DIR)
    print("Initialized repository: {}.".format(SL_DIST_REPO_DIR))
    initialFreeze = True 
else:
    repoDist = Repo(SL_DIST_REPO_DIR)
    print("Loaded existing repository: {}.".format(SL_DIST_REPO_DIR))

def freeze():
    print("Changes detected. Freezing...")
    do_freeze()
    print("Preparing to commit new frozen version...")
    upload_freeze(platformToDir[platform.system()])

if initialFreeze:
    freeze()

commitSHA = repo.head.reference.log()[0]


while True:
    print("Sleeping for 30 seconds...")
    sleep(30)

    print("Checking for changes...")
    repo.remotes.origin.pull(rebase=True)
    newCommitSHA = repo.head.reference.log()[0]

    if commitSHA != newCommitSHA:
        freeze()
    commitSHA = newCommitSHA
