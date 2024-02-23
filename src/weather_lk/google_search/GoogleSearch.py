import os
import time
from functools import cached_property

from googlesearch import search
from utils import Log

from utils_future import RemotePDF
from weather_lk.constants import DIR_REPO_PDF_GOOGLE_SEARCH

log = Log('GoogleSearch')


class GoogleSearch:
    NUM_RESULTS = 10
    SLEEP_INTERVAL = 1
    T_WAIT = 10

    @cached_property
    def pdf_link_list(self):
        search_term = "meteo.gov.lk/images/mergepdf filetype:pdf"
        pdf_link_list = [
            x
            for x in search(
                search_term,
                num_results=GoogleSearch.NUM_RESULTS,
                sleep_interval=GoogleSearch.SLEEP_INTERVAL,
            )
        ]
        log.info(f'Found {len(pdf_link_list)} pdf links.')
        return pdf_link_list

    def download_all(self):
        if not os.path.exists(DIR_REPO_PDF_GOOGLE_SEARCH):
            os.makedirs(DIR_REPO_PDF_GOOGLE_SEARCH)

        for pdf_link in self.pdf_link_list:
            RemotePDF(pdf_link).download(DIR_REPO_PDF_GOOGLE_SEARCH)
            log.debug(f'😴 Sleeping for {GoogleSearch.T_WAIT}s')
            time.sleep(GoogleSearch.T_WAIT)
