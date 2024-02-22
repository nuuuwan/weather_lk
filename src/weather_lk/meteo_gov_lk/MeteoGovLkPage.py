from functools import cached_property
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import WWW, Log
from utils_future import file_hash
from weather_lk.constants import DIR_REPO_METEO_GOV_LK_PDF
import os
import tempfile
import time

log = Log('weather_lk')


class MeteoGovLkPage:
    URL = 'http://meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 240
    T_WAIT = 4

    @staticmethod
    def download_link(pdf_url, dir_download):
        if not os.path.exists(dir_download):
            os.makedirs(dir_download)

        temp_file_path = tempfile.mktemp('.pdf')
        log.debug(f'{temp_file_path=}')
        
        WWW.download_binary(pdf_url, temp_file_path)
        
        h32 = file_hash(temp_file_path)
        log.debug(f'{h32=}')
        
        file_path = os.path.join(
            dir_download, f'{h32}.pdf'
        )
        os.rename(temp_file_path, file_path)
        log.info(f'Downloaded {pdf_url} to {file_path}')

    @cached_property 
    def pdf_url(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

        log.debug(f'Browsing {self.URL}...')
        browser.get(self.URL)
        log.debug(f'😴 Sleeping for {MeteoGovLkPage.T_WAIT}s...')
        time.sleep(MeteoGovLkPage.T_WAIT)

        a_daily = browser.find_element(
            "xpath", "//a[text()='Daily Rainfall']"
        )
        pdf_url = a_daily.get_attribute('href')
        log.debug(f'{pdf_url=}')
        browser.quit()
        return pdf_url

    def download(self):
        MeteoGovLkPage.download_link(self.pdf_url, DIR_REPO_METEO_GOV_LK_PDF)


       