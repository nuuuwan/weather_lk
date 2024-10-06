import time
from functools import cached_property

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import Log

from utils_future import RemotePDF
from weather_lk.core import Data

log = Log('weather_lk')


class MeteoGovLkPage:
    URL = 'http://meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 240
    T_WAIT = 4

    @cached_property
    def pdf_url(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(MeteoGovLkPage.PAGE_LOAD_TIMEOUT)

        log.debug(f'Browsing {MeteoGovLkPage.URL}...')
        browser.get(self.URL)
        log.debug(f'😴 Sleeping for {MeteoGovLkPage.T_WAIT}s...')
        time.sleep(MeteoGovLkPage.T_WAIT)

        a_daily = browser.find_element(
            "xpath", "//a[text()='DAILY WEATHER SUMMARY']"
        )
        pdf_url = a_daily.get_attribute('href')
        log.debug(f'{pdf_url=}')
        browser.quit()
        return pdf_url

    def download(self):
        RemotePDF(self.pdf_url).download(Data.DIR_REPO_PDF_METEO_GOV_LK)
