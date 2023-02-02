from functools import cached_property

import camelot
from utils import JSONFile, TimeFormat

from weather_lk._utils import log


class WeatherReportPDFParserMixin:
    @property
    def table_file_path(self):
        return self.file_path[:-4] + '.csv'

    @property
    def table(self):
        pdf_file = self.file_path
        tables = camelot.read_pdf(pdf_file, pages='all')
        tables.export(self.table_file_path, f='csv')
        log.info(f'Wrote {self.table_file_path}')
        table = tables[0].df.values.tolist()
        return table

    @property
    def weather_data_file_path(self):
        return self.file_path[:-4] + '.json'

    @cached_property
    def min_temp(self):
        min_temp = None
        min_temp_place = None

        weather_list = self.weather_list
        for weather in weather_list:
            place = weather.get('place')
            _min_temp = weather.get('min_temp')

            if _min_temp is not None and (
                min_temp is None or min_temp > _min_temp
            ):
                min_temp = _min_temp
                min_temp_place = place

        return dict(
            min_temp=min_temp,
            min_temp_place=min_temp_place,
        )

    @cached_property
    def max_temp(self):
        max_temp = None
        max_temp_place = None

        weather_list = self.weather_list
        for weather in weather_list:
            place = weather.get('place')
            _max_temp = weather.get('max_temp')

            if _max_temp is not None and (
                max_temp is None or max_temp < _max_temp
            ):
                max_temp = _max_temp
                max_temp_place = place

        return dict(
            max_temp=max_temp,
            max_temp_place=max_temp_place,
        )

    @cached_property
    def max_rain(self):
        max_rain = None
        max_rain_place = None

        weather_list = self.weather_list
        for weather in weather_list:
            place = weather.get('place')
            rain = weather.get('rain')

            if rain is not None and (max_rain is None or max_rain < rain):
                max_rain = rain
                max_rain_place = place

        return dict(
            max_rain=max_rain,
            max_rain_place=max_rain_place,
        )

    @cached_property
    def weather_data(self):
        weather_list_ut = self.weather_list_ut
        date_id = TimeFormat('%Y-%m-%d').stringify(weather_list_ut)
        date_id_now = self.date_id
        if date_id != date_id_now:
            raise Exception(f'Invalid date: {date_id} != {date_id_now}')

        weather_data = dict(
            date_ut=weather_list_ut,
            date=date_id,
            min_temp=self.min_temp,
            max_temp=self.max_temp,
            max_rain=self.max_rain,
            weather_list=self.weather_list,
        )
        JSONFile(self.weather_data_file_path).write(weather_data)
        return weather_data
