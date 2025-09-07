import time
from functools import cached_property

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from utils import Log

from utils_future import RemotePDF
from weather_lk.core import Data

log = Log("weather_lk")


class MeteoGovLkPageException(Exception):
    pass


class MeteoGovLkPage:
    URL = "https://meteo.gov.lk/"
    PAGE_LOAD_TIMEOUT = 240
    T_WAIT = 30

    @cached_property
    def pdf_url(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(MeteoGovLkPage.PAGE_LOAD_TIMEOUT)

        try:
            log.debug(f"Browsing {MeteoGovLkPage.URL}...")
            browser.get(self.URL)

            time.sleep(MeteoGovLkPage.T_WAIT)

            log.debug("Clicking button 'Weather Data'...")
            button_weather_data = browser.find_element(
                By.XPATH, "//button[contains(text(), 'Weather Data')]"
            )
            if not button_weather_data:
                raise MeteoGovLkPageException(
                    "Button 'Weather Data' not found."
                )
            button_weather_data.click()
            time.sleep(MeteoGovLkPage.T_WAIT)

            a_weather_report = browser.find_element(
                By.XPATH, "//a[text()='Weather Report for the 24hour Period']"
            )
            if not a_weather_report:
                raise MeteoGovLkPageException(
                    "Link 'Weather Report for the 24hour Period' not found."
                )
            log.debug("Found a_weather_report.")
            pdf_url = a_weather_report.get_attribute("href")
            log.debug(f"{pdf_url=}")
            return pdf_url

        finally:
            browser.quit()

    def download(self):
        RemotePDF(self.pdf_url).download(Data.DIR_REPO_PDF_METEO_GOV_LK)
