import os
import re
from functools import cached_property

from utils import TIME_FORMAT_DATE, JSONFile, Log, Time, TimeFormat

from weather_lk.constants import DIR_REPO_JSON_PARSED
from weather_lk.meteo_gov_lk.REGEX import REGEX
from weather_lk.place_to_latlng.PlaceToLatLng import (DEFAULT_LATLNG,
                                                      PlaceToLatLng)

log = Log('PDFParserExpandedData')


class PDFParserExpandedData:
    @cached_property
    def date_ut(self):
        for row in self.table:
            row = self.clean_row(row)
            row_str = ' '.join(row)
            result = re.search(REGEX.DATE, row_str)
            if result:
                date_str = result.groupdict().get('date_str')
                return TimeFormat('%Y.%m.%d').parse(date_str).ut
        return None

    @cached_property
    def weather_list(self):
        weather_list = []
        for row in self.table:
            weather_list += self.parse_row(row)

        PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
        expanded_weather_list = []
        for d in weather_list:
            expanded_d = d
            place = d['place']
            lat, lng = PLACE_TO_LATLNG.get(place, DEFAULT_LATLNG)
            expanded_d['lat'] = lat
            expanded_d['lng'] = lng
            expanded_weather_list.append(expanded_d)

        n = len(expanded_weather_list)
        log.debug(f'Parsed weather_list for {n} places')

        return expanded_weather_list

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
    def expanded_data(self):
        date_ut = self.date_ut
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        log.debug(f'{date=}')

        expanded_data = dict(
            date_ut=date_ut,
            date=date,
            min_temp=self.min_temp,
            max_temp=self.max_temp,
            max_rain=self.max_rain,
            weather_list=self.weather_list,
        )
        return expanded_data

    def write_json(self):
        expanded_data = self.expanded_data
        date_ut = expanded_data['date_ut']
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        if not os.path.exists(DIR_REPO_JSON_PARSED):
            os.makedirs(DIR_REPO_JSON_PARSED)
        data_path = os.path.join(DIR_REPO_JSON_PARSED, f'{date}.json')

        JSONFile(data_path).write(self.expanded_data)
        log.info(f'Wrote to data to {data_path}')
        return date, data_path
