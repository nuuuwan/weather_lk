import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import WWW, File, Log, get_date_id

from weather_lk.constants import DIR_REPO_DAILY_DATA

log = Log('weather_lk')


class DownloaderMixin:
    URL = 'http://meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 240

    @property
    def date_id(self):
        return get_date_id()

    @property
    def file_path(self):
        return os.path.join(
            DIR_REPO_DAILY_DATA, f'weather_lk.{self.date_id}.pdf'
        )

    @property
    def file(self):
        return File(self.file_path)

    def download(self):
        if self.file.exists:
            log.warning(f'{self.file_path} exists. Not downloading')
            return

        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

        log.debug(f'Browsing {self.URL}...')
        browser.get(self.URL)
        browser.implicitly_wait(5)

        a_daily = browser.find_element(
            "xpath", "//a[text()='Daily Rainfall']"
        )
        pdf_url = a_daily.get_attribute('href')
        log.debug(f'{pdf_url=}')
        browser.quit()

        WWW.download_binary(pdf_url, self.file_path)
        log.info(f'Downloaded {pdf_url} to {self.file_path}')
