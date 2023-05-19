import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import WWW, File, get_date_id

from weather_lk._utils import log


class DownloaderMixin:
    URL = 'https://www.meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 240

    @property
    def date_id(self):
        return get_date_id()

    @property
    def file_path(self):
        return f'/tmp/weather_lk.{self.date_id}.pdf'

    @property
    def file(self):
        return File(self.file_path)

    def download(self):
        if self.file.exists:
            log.warning(f'{self.file_path} exists. Not downloading')
            return

        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

        log.debug(f'Browsing {self.URL}...')
        browser.get(self.URL)
        time.sleep(5)

        a_daily = browser.find_element(
            "xpath", "//a[text()='Daily Rainfall']"
        )
        pdf_url = a_daily.get_attribute('href')
        log.debug(f'{pdf_url=}')
        browser.quit()

        WWW.download_binary(pdf_url, self.file_path)
        log.info(f'Downloaded {pdf_url} to {self.file_path}')
