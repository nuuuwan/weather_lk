import os

from utils import WWW, JSONFile, Log

log = Log('weather_lk')

class LoaderMixin:
    @property
    def remote_weather_data_url(self):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan',
            'weather_lk',
            'data',
            f'weather_lk.{self.date_id}.json',
        )

    def load_local(self):
        print(self.weather_data_file_path)
        local_file = JSONFile(self.weather_data_file_path)
        if not local_file.exists:
            return None
        data = local_file.read()
        n_places = len(data['weather_list'])
        log.info(
            f'Loaded data for {n_places} locally,'
            + f' from {self.weather_data_file_path}'
        )
        return data

    def load_remote(self):
        www = WWW(self.remote_weather_data_url)
        if not www.exists:
            return None
        data = www.readJSON()
        n_places = len(data['weather_list'])
        log.info(
            f'Loaded data for {n_places} remotely,'
            + f' from {self.remote_weather_data_url}'
        )
        return data

    def load(self):
        data = self.load_local()
        if data:
            return data
        data = self.load_remote()
        if data:
            return data
        log.error('No data for %s', self.date_id)
        return None
