import time
from functools import cached_property

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

        wait = WebDriverWait(browser, MeteoGovLkPage.PAGE_LOAD_TIMEOUT)
        button_weather_data = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Weather Data']")
            )
        )
        log.debug("Clicking button 'Weather Data'...")
        button_weather_data.click()

        a_weather_report = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[text()='Weather Report for the 24hour Period']",
                )
            )
        )
        log.debug("Found a_weather_report.")
        pdf_url = a_weather_report.get_attribute("href")
        log.debug(f"{pdf_url=}")
        return pdf_url

    def download(self):
        RemotePDF(self.pdf_url).download(Data.DIR_REPO_PDF_METEO_GOV_LK)
