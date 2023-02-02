from utils import JSONFile, WWW
from weather_lk._utils import log
import os


class WeatherReportPDFLoaderMixin:
    @property
    def remote_weather_data_url(self):
        return os.path.join(
            'https://raw.githubusercontent.com',
            'nuuuwan',
            'weather_lk',
            'data',
            f'weather_lk.{self.date_id}.json',
        )

    def load(self):
        local_file = JSONFile(self.weather_data_file_path)
        if local_file.exists:
            data = local_file.read()
            n_places = len(data['weather_list'])
            log.info(
                f'Loaded data for {n_places} locally,'
                + f' from {self.weather_data_file_path}'
            )
            return data

        www = WWW(self.remote_weather_data_url)
        if www.exists:
            data = www.readJSON()
            n_places = len(data['weather_list'])
            log.info(
                f'Loaded data for {n_places} remotely,'
                + f' from {self.remote_weather_data_url}'
            )
            return data

        log.error('No data for %s', self.date_id)
        return None
