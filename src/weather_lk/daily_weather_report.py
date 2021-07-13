"""Daily Weather Report."""

import os
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import timex, www

from weather_lk._constants import REGEX_DATE_URL, URL
from weather_lk._utils import log
from weather_lk.daily_weather_report_parse import _parse_and_dump


def _scrape_latest():
    """Get daily weather report."""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    a_daily = browser.find_element_by_xpath("//a[text()='Daily Rainfall']")
    pdf_url = a_daily.get_attribute('href')
    browser.quit()

    result = re.search(REGEX_DATE_URL, pdf_url)
    if result:
        result_data = result.groupdict()
        unixtime = timex.parse_time(
            '%s-%s-%s'
            % (
                result_data['date_y'],
                result_data['date_m'],
                result_data['date_d'],
            ),
            '%Y-%m-%d',
        )
    else:
        unixtime = timex.get_unixtime()

    date_id = timex.format_time(unixtime, '%Y%m%d')
    pdf_file = '/tmp/weather_lk.%s.pdf' % (date_id)
    www.download_binary(pdf_url, pdf_file)
    log.info('%s: Downloaded %s to %s', date_id, pdf_url, pdf_file)

    return date_id, pdf_file


def _dump_latest():
    """Scrape and parse daily weather report."""
    date_id, pdf_file = _scrape_latest()
    _parse_and_dump(date_id, pdf_file)


def _load(date_id):
    """Load daily weather report."""
    url = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan/weather_lk/data',
        'weather_lk.%s.json' % date_id,
    )
    if not www.exists(url):
        log.error('No data for %s', date_id)
        return None
    return www.read_json(url)
