"""Uploaded data to nuuuwan/weather_lk:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/weather_lk.test.txt')
    os.system('echo "# weather_lk" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
