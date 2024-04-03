import os
import time

from utils import JSONFile, Log

from weather_lk.core import Data
from weather_lk.constants import TEST_MODE

log = Log('PDFParserGlobal')


class PDFParserGlobal:
    MAX_RUNNING_TIME = 1 if TEST_MODE else 60 * (15 - 5)
    PDF_DIR_LIST = [
        Data.DIR_REPO_PDF_METEO_GOV_LK,
        Data.DIR_REPO_PDF_ARCHIVE_ORG,
        Data.DIR_REPO_PDF_GOOGLE_SEARCH,
    ]

    @staticmethod
    def is_valid_pdf(pdf_name):
        if not pdf_name.endswith('.pdf'):
            return False
        if len(pdf_name) != 32 + 4:
            return False
        return True

    @staticmethod
    def source_to_file_name():
        source_to_file_name = {}
        for dir in PDFParserGlobal.PDF_DIR_LIST:
            source_id = os.path.basename(dir)
            if source_id not in source_to_file_name:
                source_to_file_name[source_id] = []

            for file_name in os.listdir(dir):
                if not PDFParserGlobal.is_valid_pdf(file_name):
                    continue
                source_to_file_name[source_id].append(file_name)

        return source_to_file_name

    @staticmethod
    def source_to_pdf_paths():
        source_to_pdf_paths = {}
        for (
            source_id,
            file_names,
        ) in PDFParserGlobal.source_to_file_name().items():
            dir = os.path.join(DIR_REPO, source_id)
            for file_name in file_names:
                pdf_path = os.path.join(dir, file_name)
                if source_id not in source_to_pdf_paths:
                    source_to_pdf_paths[source_id] = []
                source_to_pdf_paths[source_id].append(pdf_path)

        return source_to_pdf_paths

    @staticmethod
    def get_pdf_paths():
        pdf_paths = []
        for (
            pdf_paths_for_source
        ) in PDFParserGlobal.source_to_pdf_paths().values():
            pdf_paths.extend(pdf_paths_for_source)
        return pdf_paths

    @classmethod
    def parse_one(cls, pdf_path):
        try:
            parser = cls(pdf_path)
            if parser.is_parsed:
                return 0

            date, data_path = parser.write_json()
            parser.write_placeholder_json(date, data_path)
            return 1
        except Exception as e:
            log.error(f'PDFParser.parse_one({pdf_path}): {str(e)}')
            parser.write_placeholder_json('unknown', 'unknown')
            return 2

    @staticmethod
    def cleanup_bad_runs():
        bad_path_list = []
        n = 0
        for file_name in os.listdir(Data.DIR_REPO_JSON_PLACEHOLDER):
            if not file_name.endswith('.json'):
                continue
            file_path = os.path.join(
                Data.DIR_REPO_JSON_PLACEHOLDER, file_name
            )
            data = JSONFile(file_path).read()
            if data['date'] == 'unknown':
                bad_path_list.append(file_path)
            n += 1
        n_bad = len(bad_path_list)
        for file_path in bad_path_list:
            os.remove(file_path)
            log.debug(f'Removed {file_path}')
        log.info(f'Cleaned up {n_bad}/{n}.')

    @classmethod
    def parse_all(cls):
        t_start = time.time()

        Data.init()
        # HACK - PDFParserGlobal.cleanup_bad_runs()

        pdf_list = cls.get_pdf_paths()

        n = len(pdf_list)
        n_old, n_new, n_fail = 0, 0, 0
        for pdf_path in pdf_list:
            result = cls.parse_one(pdf_path)
            if result == 0:
                n_old += 1
            elif result == 1:
                n_new += 1
            else:
                n_fail += 1
            dt = time.time() - t_start
            if dt > cls.MAX_RUNNING_TIME:
                log.info(f'Stopping ({cls.MAX_RUNNING_TIME}s < {dt:.3f}s).')
                break

        log.info(f'Parsed {n_new} new pdfs.')
        log.debug(f'{n=}, {n_old=}, {n_fail=}')
