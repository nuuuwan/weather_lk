from weather_lk.constants import BRANCH_NAME, DIR_REPO, GIT_REPO_URL
from utils import Git


class Data:
    @staticmethod
    def init():
        git = Git(GIT_REPO_URL)
        git.clone(DIR_REPO)
        git.checkout(BRANCH_NAME)
