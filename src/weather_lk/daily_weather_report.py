"""Daily Weather Report."""

import os
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import timex, www

from weather_lk._constants import REGEX_DATE_URL, URL
from weather_lk._utils import log
from weather_lk.daily_weather_report_parse import _parse_and_dump


def get_file(date_id, ext):
    return f'/tmp/weather_lk.{date_id}.{ext}'

def scrape(date_id):
    """Get daily weather report."""
    pdf_file = get_file(date_id, pdf)
    if os.path.exists(pdf_file):
        log.warning(f'{pdf_file} exists. Not downloading')

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    a_daily = browser.find_element_by_xpath("//a[text()='Daily Rainfall']")
    pdf_url = a_daily.get_attribute('href')
    browser.quit()

    www.download_binary(pdf_url, pdf_file)
    log.info(f'Downloaded {pdf_url} to {pdf_file}')

def parse(date_id):
    pdf_file = get_file(date_id, pdf)







def load(date_id):
    """Load daily weather report."""
    url = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan/weather_lk/data',
        'weather_lk.%s.json' % date_id,
    )
    if not www.exists(url):
        log.error('No data for %s', date_id)
        return None
    return www.read_json(url)

if __name__ == '__main__':
    date_id = timex.get_date_id()
    scrape(date_id)
