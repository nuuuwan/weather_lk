import os

from utils import Log

from weather_lk.constants import (DIR_REPO_PDF_ARCHIVE_ORG,
                                  DIR_REPO_PDF_GOOGLE_SEARCH,
                                  DIR_REPO_PDF_METEO_GOV_LK)
from weather_lk.core.Data import Data

log = Log('PDFParserGlobal')


class PDFParserGlobal:
    N_MAX_PARSE = 100
    PDF_DIR_LIST = [
        DIR_REPO_PDF_METEO_GOV_LK,
        DIR_REPO_PDF_ARCHIVE_ORG,
        DIR_REPO_PDF_GOOGLE_SEARCH,
    ]
    @staticmethod
    def is_valid_pdf(pdf_name):
        if not pdf_name.endswith('.pdf'):
            return False
        if len(pdf_name) != 32 + 4:
           return False 
        return True
    
    @staticmethod
    def source_to_pdf_paths():
        source_to_pdf_paths = {}
        for dir in PDFParserGlobal.PDF_DIR_LIST:
            source_id = os.path.basename(dir)
            if source_id not in source_to_pdf_paths:
                source_to_pdf_paths[source_id] = []
                
            for file_name in os.listdir(dir):
                if not PDFParserGlobal.is_valid_pdf(file_name):
                    continue
                source_to_pdf_paths[source_id].append(os.path.join(dir, file_name))

        return source_to_pdf_paths
    
    @staticmethod
    def get_pdf_paths():
        pdf_paths = []
        for pdf_paths_for_source in PDFParserGlobal.source_to_pdf_paths().values():
            pdf_paths.extend(pdf_paths_for_source)
        return pdf_paths

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
            parser.write_placeholder_json('unknown', 'unknown')

            return False
        return True

    @classmethod
    def parse_all(cls):
        Data.init()
        pdf_list = cls.get_pdf_paths()
        i_parse = 0
        for i_pdf, pdf_path in enumerate(pdf_list):
            log.debug(f'{i_pdf+1}/{i_parse+1}) {pdf_path}')
            if cls.parse_one(pdf_path):
                i_parse += 1
                if i_parse >= PDFParserGlobal.N_MAX_PARSE:
                    break
