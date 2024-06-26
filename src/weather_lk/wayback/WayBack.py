import os
import time
from functools import cached_property

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import Log

from utils_future import RemotePDF
from weather_lk.core import Data

log = Log('WayBack')


class WayBack:
    T_WAIT = 2

    @property
    def url_index(self) -> str:
        return (
            'https://web.archive.org/web/*'
            + '/https://www.meteo.gov.lk/images/mergepdf/*'
        )

    @staticmethod
    def get_pdf_links(driver):
        pdf_link_list = []
        for elem_link_pdf in driver.find_elements(
            By.XPATH, "//a[contains(@href, '.pdf')]"
        ):
            pdf_link_list.append(elem_link_pdf.get_attribute('href'))

        log.debug(f'Found {len(pdf_link_list)} pdf links')
        return pdf_link_list

    @staticmethod
    def click_next(driver):
        try:
            elem_button_next = driver.find_element(
                By.XPATH, "//a[contains(text(), 'Next')]"
            )
            attr_disabled = elem_button_next.get_attribute('aria-disabled')
            if attr_disabled:
                log.debug('No more "Next" button found.')
                return False
            elem_button_next.click()
        except Exception as e:
            log.error(f'Wayback.click_next: {str(e)}')
            return False
        return True

    @cached_property
    def pdf_link_list(self) -> list[str]:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)
        log.debug(f'Opening {self.url_index}...')
        driver.get(self.url_index)

        all_pdf_links = []

        while True:
            log.debug(f'😴 Sleeping for {WayBack.T_WAIT}s')
            time.sleep(WayBack.T_WAIT)

            all_pdf_links.extend(WayBack.get_pdf_links(driver))

            if not WayBack.click_next(driver):
                break

        log.info(f'Found {len(all_pdf_links)} pdf links in total.')

        driver.quit()
        log.debug('Closing browser.')

        return all_pdf_links

    def download_all(self):
        if not os.path.exists(Data.DIR_REPO_PDF_ARCHIVE_ORG):
            os.makedirs(Data.DIR_REPO_PDF_ARCHIVE_ORG)

        for pdf_link in self.pdf_link_list:
            RemotePDF(pdf_link).download(Data.DIR_REPO_PDF_ARCHIVE_ORG)
            log.debug(f'😴 Sleeping for {WayBack.T_WAIT}s')
            time.sleep(WayBack.T_WAIT)
