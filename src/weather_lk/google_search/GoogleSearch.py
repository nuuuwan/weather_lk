import os
import random
import time
from functools import cached_property

from googlesearch import search
from utils import Log

from utils_future import RemotePDF
from weather_lk.core import Data

log = Log('GoogleSearch')


class GoogleSearch:
    NUM_RESULTS = 64
    SLEEP_INTERVAL = 1
    T_WAIT = 1

    @cached_property
    def random_year(self):
        return random.choice([2024, 2023, 2022])

    @cached_property
    def pdf_link_list(self):
        year = self.random_year
        search_term = "meteo.gov.lk/images/mergepdf " + f"{year} filetype:pdf"
        pdf_link_list = [
            x
            for x in search(
                search_term,
                num_results=GoogleSearch.NUM_RESULTS,
                sleep_interval=GoogleSearch.SLEEP_INTERVAL,
            )
        ]

        filtered_pdf_link_list = [
            x for x in pdf_link_list if "meteo.gov.lk/images/mergepdf" in x
        ]
        log.info(f'Found {len(pdf_link_list)} pdf links for {year=}.')

        return filtered_pdf_link_list

    def download_all(self):
        if not os.path.exists(Data.DIR_REPO_PDF_GOOGLE_SEARCH):
            os.makedirs(Data.DIR_REPO_PDF_GOOGLE_SEARCH)

        for pdf_link in self.pdf_link_list:
            RemotePDF(pdf_link).download(Data.DIR_REPO_PDF_GOOGLE_SEARCH)
            log.debug(f'😴 Sleeping for {GoogleSearch.T_WAIT}s')
            time.sleep(GoogleSearch.T_WAIT)
