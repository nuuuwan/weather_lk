import time
from functools import cached_property

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
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
    MAX_RETRIES = 3
    RETRY_DELAY = 60

    def _try_get_pdf_url(self):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.set_page_load_timeout(MeteoGovLkPage.PAGE_LOAD_TIMEOUT)

        try:
            log.debug(f"Browsing {MeteoGovLkPage.URL}...")
            browser.get(self.URL)

            time.sleep(MeteoGovLkPage.T_WAIT)

            log.debug("Clicking button with 'Weather Data'...")
            button_weather_data = browser.find_element(
                By.XPATH, "//button[contains(text(), 'Weather Data')]"
            )
            if not button_weather_data:
                raise MeteoGovLkPageException(
                    "Button with 'Weather Data' not found."
                )
            button_weather_data.click()
            time.sleep(MeteoGovLkPage.T_WAIT)

            log.debug("Clicking button 'Other Weather Data'...")
            button_other_weather_data = browser.find_element(
                By.XPATH, "//button[contains(text(), 'Other Weather Data')]"
            )
            if not button_other_weather_data:
                raise MeteoGovLkPageException(
                    "Button 'Other Weather Data' not found."
                )
            button_other_weather_data.click()
            time.sleep(MeteoGovLkPage.T_WAIT)

            a_weather_report = browser.find_element(
                By.XPATH, "//a[contains(text(), '24 Hour Weather Report')]"
            )
            if not a_weather_report:
                raise MeteoGovLkPageException(
                    "Link '24 Hour Weather Report' not found."
                )
            log.debug("Found a_weather_report.")
            pdf_url = a_weather_report.get_attribute("href")
            log.debug(f"{pdf_url=}")
            return pdf_url

        finally:
            browser.quit()

    @cached_property
    def pdf_url(self):
        last_error = None
        for attempt in range(1, MeteoGovLkPage.MAX_RETRIES + 1):
            try:
                return self._try_get_pdf_url()
            except WebDriverException as e:
                last_error = e
                log.warning(
                    f"Attempt {attempt}/{MeteoGovLkPage.MAX_RETRIES} failed: {e}"
                )
                if attempt < MeteoGovLkPage.MAX_RETRIES:
                    log.debug(
                        f"Retrying in {MeteoGovLkPage.RETRY_DELAY}s..."
                    )
                    time.sleep(MeteoGovLkPage.RETRY_DELAY)
        raise last_error

    def download(self):
        RemotePDF(self.pdf_url).download(Data.DIR_REPO_PDF_METEO_GOV_LK)
