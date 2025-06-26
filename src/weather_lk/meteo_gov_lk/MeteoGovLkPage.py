import time
from functools import cached_property

from selenium import webdriver
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

        log.debug(f"Browsing {MeteoGovLkPage.URL}...")
        browser.get(self.URL)

        log.debug(f"😴 Sleeping for {MeteoGovLkPage.T_WAIT}s...")
        time.sleep(MeteoGovLkPage.T_WAIT)

        button_weather_data = browser.find_element(
            "xpath",
            "//button[text()='Weather Data']",
        )
        if not button_weather_data:
            raise MeteoGovLkPageException("Button 'Weather Data' not found.")
        log.debug("Clicking button 'Weather Data'...")
        button_weather_data.click()

        log.debug(f"😴 Sleeping for {MeteoGovLkPage.T_WAIT}s...")
        time.sleep(MeteoGovLkPage.T_WAIT)

        a_weather_report = browser.find_element(
            "xpath",
            "//a[text()='Weather Report for the 24hour Period']",
        )
        if not a_weather_report:
            raise MeteoGovLkPageException(
                "Link 'Weather Report for the 24hour Period' not found."
            )
        log.debug("Found a_weather_report.")
        pdf_url = MeteoGovLkPage.URL + a_weather_report.get_attribute("href")
        log.debug(f"{pdf_url=}")
        return pdf_url

    def download(self):
        RemotePDF(self.pdf_url).download(Data.DIR_REPO_PDF_METEO_GOV_LK)
