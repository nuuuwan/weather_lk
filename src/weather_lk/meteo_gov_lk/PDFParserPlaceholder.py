import os
from functools import cached_property

from utils import JSONFile, Log

from weather_lk.core import Data

log = Log('PDFParserPlaceholder')


class PDFParserPlaceholder:
    @staticmethod
    def get_placeholder_path(file_id):
        return os.path.join(Data.DIR_REPO_JSON_PLACEHOLDER, f'{file_id}.json')

    @cached_property
    def placeholder_path(self):
        file_id = self.pdf_path.split(os.sep)[-1].split('.')[0]
        return PDFParserPlaceholder.get_placeholder_path(file_id)

    @cached_property
    def is_parsed(self):
        return os.path.exists(self.placeholder_path)

    def write_placeholder_json(self, date, data_path):
        if not os.path.exists(Data.DIR_REPO_JSON_PLACEHOLDER):
            os.makedirs(Data.DIR_REPO_JSON_PLACEHOLDER)
        placeholder_path = self.placeholder_path
        JSONFile(placeholder_path).write(
            dict(
                date=date,
                data_path=data_path,
                placeholder_path=placeholder_path,
            )
        )
        log.debug(f'Wrote placeholder to {placeholder_path}')
