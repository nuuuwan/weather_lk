import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import WWW, Log, hashx

from weather_lk.constants import DIR_REPO_METEO_GOV_LK_PDF

log = Log('weather_lk')


class PDFDownload:
    URL = 'http://meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 240
    T_WAIT = 10

    def download(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

        log.debug(f'Browsing {self.URL}...')
        browser.get(self.URL)
        log.debug(f'😴 Sleeping for {PDFDownload.T_WAIT}s...')
        time.sleep(PDFDownload.T_WAIT)

        a_daily = browser.find_element(
            "xpath", "//a[text()='Daily Rainfall']"
        )
        pdf_url = a_daily.get_attribute('href')
        log.debug(f'{pdf_url=}')
        browser.quit()

        h = hashx.md5(pdf_url + get_date_id())

        if not os.path.exists(DIR_REPO_METEO_GOV_LK_PDF):
            os.makedirs(DIR_REPO_METEO_GOV_LK_PDF)
        
        file_path = os.path.join(
            DIR_REPO_METEO_GOV_LK_PDF, f'meteo_gov_lk.{h}.pdf'
        )

        WWW.download_binary(pdf_url, file_path)
        log.info(f'Downloaded {pdf_url} to {file_path}')
