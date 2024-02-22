import os
import re
from functools import cached_property

import camelot
from utils import TIME_FORMAT_DATE, JSONFile, Log, String, Time, TimeFormat

from weather_lk.constants import (
    DIR_REPO_JSON_PARSED,
    DIR_REPO_JSON_PLACEHOLDER,
    DIR_REPO_PDF_ARCHIVE_ORG,
    DIR_REPO_PDF_METEO_GOV_LK,
)
from weather_lk.core.Data import Data
from weather_lk.meteo_gov_lk.REGEX import REGEX
from weather_lk.place_to_latlng.PlaceToLatLng import (
    DEFAULT_LATLNG,
    PlaceToLatLng,
)

log = Log('weather_lk')


class PDFParser:
    N_MAX_PARSE = 64

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    @cached_property
    def table(self):
        tables = camelot.read_pdf(self.pdf_path, pages='all')
        table = tables[0].df.values.tolist()
        return table

    def clean_cell(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        return cell

    def clean_row(self, row):
        return [self.clean_cell(cell) for cell in row]

    def clean_location_name(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        cell = cell.replace('wkqrdOmqrh', '')
        cell = cell.replace('polonnaruwa', 'Polonnaruwa')
        cell = cell.replace('Stations', ' ')
        cell = cell.replace('Station', ' ')
        cell = ' '.join(
            list(
                filter(
                    lambda word: len(word) > 0
                    and (word[0] != word[0].lower()),
                    cell.split(' '),
                )
            )
        )
        return cell

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

    def parse_single_place_row(self, row):
        place_str, max_temp_str, min_temp_str, rain_str, _ = row
        place = self.clean_location_name(place_str)
        min_temp = String(min_temp_str).float
        max_temp = String(max_temp_str).float
        rain = String(rain_str).float

        if rain is None:
            return []

        return [
            dict(
                place=place,
                min_temp=min_temp,
                max_temp=max_temp,
                rain=rain,
            )
        ]

    def parse_double_place_row(self, row):
        place_str1, rain_str1, place_str2, _, rain_str2 = row
        place1 = self.clean_location_name(place_str1)
        place2 = self.clean_location_name(place_str2)
        rain1 = String(rain_str1).float
        rain2 = String(rain_str2).float

        weather_list = []
        if rain1 is not None:
            weather_list.append(
                dict(
                    place=place1,
                    rain=rain1,
                    min_temp=None,
                    max_temp=None,
                )
            )
        if rain2 is not None:
            weather_list.append(
                dict(
                    place=place2,
                    rain=rain2,
                    min_temp=None,
                    max_temp=None,
                )
            )
        return weather_list

    def parse_row(self, row):
        row = self.clean_row(row)

        weather_list = []

        if re.search(REGEX.DATE, ' '.join(row)):
            pass
        elif row[0] != '' and row[-1] == '':
            weather_list = self.parse_single_place_row(row)
        elif row[0] != '' and row[-2] == '':
            weather_list = self.parse_double_place_row(row)

        return weather_list

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
    def weather_data(self):
        date_ut = self.date_ut
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        log.debug(f'{date=}')

        weather_data = dict(
            date_ut=date_ut,
            date=date,
            min_temp=self.min_temp,
            max_temp=self.max_temp,
            max_rain=self.max_rain,
            weather_list=self.weather_list,
        )
        return weather_data

    def write_json(self):
        weather_data = self.weather_data
        date_ut = weather_data['date_ut']
        date = TIME_FORMAT_DATE.stringify(Time(date_ut))
        if not os.path.exists(DIR_REPO_JSON_PARSED):
            os.makedirs(DIR_REPO_JSON_PARSED)
        data_path = os.path.join(DIR_REPO_JSON_PARSED, f'{date}.json')

        JSONFile(data_path).write(self.weather_data)
        log.info(f'Wrote to data to {data_path}')
        return date, data_path

    @cached_property
    def placeholder_path(self):
        file_id = self.pdf_path.split(os.sep)[-1].split('.')[0]
        return os.path.join(DIR_REPO_JSON_PLACEHOLDER, f'{file_id}.json')

    @cached_property
    def is_parsed(self):
        return os.path.exists(self.placeholder_path)

    def write_placeholder_json(self, date, data_path):
        if not os.path.exists(DIR_REPO_JSON_PLACEHOLDER):
            os.makedirs(DIR_REPO_JSON_PLACEHOLDER)
        placeholder_path = self.placeholder_path
        JSONFile(placeholder_path).write(
            dict(
                date=date,
                data_path=data_path,
                placeholder_path=placeholder_path,
            )
        )
        log.debug(f'Wrote placeholder to {placeholder_path}')

    @staticmethod
    def get_pdf_paths():
        pdf_list = []
        for dir in [DIR_REPO_PDF_METEO_GOV_LK, DIR_REPO_PDF_ARCHIVE_ORG]:
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

    @staticmethod
    def parse_one(pdf_path):
        try:
            parser = PDFParser(pdf_path)
            if parser.is_parsed:
                log.debug(f'{pdf_path} is already parsed')
                return False
            date, data_path = parser.write_json()
            parser.write_placeholder_json(date, data_path)
        except Exception as e:
            log.error(str(e))
            return False
        return True

    @staticmethod
    def parse_all():
        Data.init()
        pdf_list = PDFParser.get_pdf_paths()
        i_parse = 0
        for pdf_path in pdf_list:
            if PDFParser.parse_one(pdf_path):
                i_parse += 1
                log.debug(f'{i_parse=}')
                if i_parse >= PDFParser.N_MAX_PARSE:
                    break


def test():
    PDFParser.parse_all()


if __name__ == "__main__":
    test()
