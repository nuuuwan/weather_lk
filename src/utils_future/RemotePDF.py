import os
import tempfile

from utils import WWW, Hash, Log

log = Log('weather_lk')


class RemotePDF:
    T_WAIT = 4

    @staticmethod
    def file_hash(file_path) -> str:
        with open(file_path, 'rb') as f:
            file_content = f.read().decode('utf-8', errors='ignore')
            h32 = Hash.md5(file_content)
            return h32

    def __init__(self, pdf_url):
        self.pdf_url = pdf_url

    def download(self, dir_download):
        if not os.path.exists(dir_download):
            os.makedirs(dir_download)

        temp_file_path = tempfile.mktemp('.pdf')
        log.debug(f'{temp_file_path=}')

        try:
            WWW(self.pdf_url).download_binary(temp_file_path)
        except Exception as e:
            log.error(f'RemotePDF({self.pdf_url}).download(): {str(e)}')
            return

        h32 = RemotePDF.file_hash(temp_file_path)
        log.debug(f'{h32=}')

        file_path = os.path.join(dir_download, f'{h32}.pdf')
        if not os.path.exists(file_path):
            os.rename(temp_file_path, file_path)
            log.info(f'Downloaded {self.pdf_url} to {file_path}')
        else:
            log.debug(f'{file_path} exists')

