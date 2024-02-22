"""Daily Weather Report."""

from utils import Git

from weather_lk import Summary, Tweeter, WeatherReport
from weather_lk.constants import BRANCH_NAME, DIR_REPO, GIT_REPO_URL


def init():
    git = Git(GIT_REPO_URL)
    git.clone(DIR_REPO)
    git.checkout(BRANCH_NAME)


def main():
    init()

    weather_report = WeatherReport()
    weather_report.download()

    s = Summary()
    s.write()
    s.write_by_place()
    s.draw_charts_by_place()

    tweeter = Tweeter(weather_report)
    tweeter.send()


if __name__ == "__main__":
    main()
