import os
import time
from functools import cached_property

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import WWW, Log, hashx

from weather_lk.constants import DIR_REPO_WAYBACK_DATA

log = Log('WayBack')


class WayBack:
    T_WAIT = 4

    @property
    def url_index(self) -> str:
        return (
            'https://web.archive.org/web/*'
            + '/https://www.meteo.gov.lk/images/mergepdf/*'
        )

    @cached_property
    def pdf_link_list(self) -> list[str]:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)
        log.debug(f'Opening {self.url_index}...')
        driver.get(self.url_index)

        all_pdf_links = []

        while True:
            log.debug(f'😴 waiting for {WayBack.T_WAIT}s')
            time.sleep(WayBack.T_WAIT)

            pdf_link_list = []
            for elem_link_pdf in driver.find_elements(
                By.XPATH, "//a[contains(@href, '.pdf')]"
            ):
                pdf_link_list.append(elem_link_pdf.get_attribute('href'))

            log.debug(f'Found {len(pdf_link_list)} pdf links')
            all_pdf_links.extend(pdf_link_list)

            try:
                elem_button_next = driver.find_element(
                    By.XPATH, "//a[contains(text(), 'Next')]"
                )
                attr_disabled = elem_button_next.get_attribute(
                    'aria-disabled'
                )
                if attr_disabled:
                    log.debug('No more "Next" button found.')
                    break
                elem_button_next.click()
            except Exception as e:
                log.error(str(e))
                break

        log.info(f'Found {len(all_pdf_links)} pdf links in total.')

        driver.quit()
        log.debug('Closing browser.')

        return pdf_link_list

    @staticmethod
    def download_one(pdf_link: str):
        h = hashx.md5(pdf_link)
        file_path = os.path.join(DIR_REPO_WAYBACK_DATA, f'wayback.{h}.pdf')
        WWW.download_binary(pdf_link, file_path)
        log.info(f'Downloaded {pdf_link} to {file_path}')

    def download_all(self):
        if not os.path.exists(DIR_REPO_WAYBACK_DATA):
            os.makedirs(DIR_REPO_WAYBACK_DATA)

        for pdf_link in self.pdf_link_list:
            WayBack.download_one(pdf_link)
