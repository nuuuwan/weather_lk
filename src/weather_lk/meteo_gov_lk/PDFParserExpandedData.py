import os
import re
import shutil
from functools import cached_property

from utils import TIME_FORMAT_DATE, JSONFile, Log, Time, TimeFormat

from weather_lk.core import Data
from weather_lk.meteo_gov_lk.REGEX import REGEX
from weather_lk.place_to_latlng import PlaceToLatLng

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
            lat, lng = PLACE_TO_LATLNG.get(
                place, PlaceToLatLng.DEFAULT_LATLNG
            )
            expanded_d['lat'] = lat
            expanded_d['lng'] = lng
            expanded_weather_list.append(expanded_d)

        n = len(expanded_weather_list)
        log.debug(f'Parsed weather_list for {n} places')

        return expanded_weather_list

    @cached_property
    def max_rain(self):
        place_and_max = [
            [
                weather.get('place'),
                weather.get('rain'),
            ]
            for weather in self.weather_list
        ]
        sorted_max = sorted(place_and_max, key=lambda x: x[1], reverse=True)

        max_rain = sorted_max[0][1]
        max_rain_place = sorted_max[0][0]

        return dict(
            max_rain=max_rain,
            max_rain_place=max_rain_place,
        )

    @cached_property
    def min_max_temp(self):
        place_min_and_max = [
            [
                weather.get('place'),
                weather.get('min_temp'),
                weather.get('max_temp'),
            ]
            for weather in self.weather_list
            if weather.get('min_temp') and weather.get('max_temp')
        ]
        sorted_min = sorted(place_min_and_max, key=lambda x: x[1])
        min_temp = sorted_min[0][1]
        min_temp_place = sorted_min[0][0]

        sorted_max = sorted(
            place_min_and_max, key=lambda x: x[2], reverse=True
        )
        max_temp = sorted_max[0][2]
        max_temp_place = sorted_max[0][0]

        return dict(
            min_temp=dict(
                min_temp=min_temp,
                min_temp_place=min_temp_place,
            ),
            max_temp=dict(
                max_temp=max_temp,
                max_temp_place=max_temp_place,
            ),
        )

    @cached_property
    def expanded_data(self):
        date_ut = self.date_ut
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        log.debug(f'{date=}')

        expanded_data = (
            dict(
                pdf_path=self.pdf_path,
                date_ut=date_ut,
                date=date,
                weather_list=self.weather_list,
                max_rain=self.max_rain,
            )
            | self.min_max_temp
        )

        return expanded_data

    def write_json(self):
        expanded_data = self.expanded_data
        date_ut = expanded_data['date_ut']
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        if not os.path.exists(Data.DIR_REPO_JSON_PARSED):
            os.makedirs(Data.DIR_REPO_JSON_PARSED)
        data_path = os.path.join(Data.DIR_REPO_JSON_PARSED, f'{date}.json')

        JSONFile(data_path).write(self.expanded_data)
        log.info(f'Wrote to data to {data_path}')

        parsed_pdf_path = os.path.join(
            Data.DIR_REPO_PDF_PARSED, f'{date}.pdf'
        )
        if not os.path.exists(Data.DIR_REPO_PDF_PARSED):
            os.makedirs(Data.DIR_REPO_PDF_PARSED)
        shutil.copyfile(self.pdf_path, parsed_pdf_path)
        log.info(f'Copied {self.pdf_path} to {parsed_pdf_path}')

        return date, data_path
