import os
import git
import shutil
import stat
from subprocess import call
import time

from configuration import Configuration


def getRepo(config: Configuration):
    # build path
    repoPath = os.path.join(
        config.repositoryPath,
        "{}.{}".format(config.repositoryOwner, config.repositoryName),
    )
    # get repository reference
    repo = None
    if not os.path.exists(repoPath):
        print("Downloading repository...")
        repo = git.Repo.clone_from(
            config.repositoryUrl,
            repoPath,
            branch="master",
            progress=Progress(),
            odbt=git.GitCmdObjectDB,
        )
        print()
    else:
        repo = git.Repo(repoPath, odbt=git.GitCmdObjectDB)

    return repo


def delete_repo(config: Configuration):

    # build path
    repoPath = os.path.join(config.repositoryPath, "{}.{}".format(
        config.repositoryOwner, config.repositoryName),)
    delete_git_folder(repoPath+"/.git")
    time.sleep(0.2)
    os.rmdir(repoPath)
    shutil.rmtree(config.repositoryPath)


def delete_git_folder(path):
    # We want to unhide the .git folder before unlinking it.
    while True:
        call(['attrib', '-H', path])
        break
    shutil.rmtree(path, onerror=on_rm_error)
    return


def on_rm_error(func, path, exc_info):
    # from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line, end="\r")
