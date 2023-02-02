from utils import get_date_id, File, WWW
from weather_lk._utils import log

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class WeatherReportPDFDownloaderMixin:
    URL = 'https://www.meteo.gov.lk/index.php?lang=en'
    PAGE_LOAD_TIMEOUT = 120

    @property
    def data_id(self):
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

        browser.get(self.URL)
        a_daily = browser.find_element(
            "xpath", "//a[text()='Daily Rainfall']"
        )
        pdf_url = a_daily.get_attribute('href')
        browser.quit()

        WWW(pdf_url).downloadBinary(self.file_path)
        log.info(f'Downloaded {pdf_url} to {self.file_path}')
