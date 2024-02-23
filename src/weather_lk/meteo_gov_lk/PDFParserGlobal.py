import os

from utils import Log

from weather_lk.constants import (DIR_REPO_PDF_ARCHIVE_ORG,
                                  DIR_REPO_PDF_GOOGLE_SEARCH,
                                  DIR_REPO_PDF_METEO_GOV_LK)
from weather_lk.core.Data import Data

log = Log('PDFParserGlobal')


class PDFParserGlobal:
    N_MAX_PARSE = 100

    @staticmethod
    def get_pdf_paths():
        pdf_list = []
        for dir in [
            DIR_REPO_PDF_METEO_GOV_LK,
            DIR_REPO_PDF_ARCHIVE_ORG,
            DIR_REPO_PDF_GOOGLE_SEARCH,
        ]:
            if not os.path.exists(dir):
                continue
            for file_name in os.listdir(dir):
                if not (
                    file_name.endswith('.pdf') and len(file_name) == 32 + 4
                ):
                    continue
                pdf_list.append(os.path.join(dir, file_name))
        log.info(f'Found {len(pdf_list)} pdfs')
        return pdf_list

    @classmethod
    def parse_one(cls, pdf_path):
        try:
            parser = cls(pdf_path)
            if parser.is_parsed:
                log.debug(f'{pdf_path} is already parsed')
                return False
            date, data_path = parser.write_json()
            parser.write_placeholder_json(date, data_path)
        except Exception as e:
            log.error(f'PDFParser.parse_one({pdf_path}): {str(e)}')
            parser.write_placeholder_json('unknown','unknown')
            return False
        return True

    @classmethod
    def parse_all(cls):
        Data.init()
        pdf_list = cls.get_pdf_paths()
        i_parse = 0
        for pdf_path in pdf_list:
            if cls.parse_one(pdf_path):
                i_parse += 1
                log.debug(f'{i_parse=}')
                if i_parse >= PDFParserGlobal.N_MAX_PARSE:
                    break
