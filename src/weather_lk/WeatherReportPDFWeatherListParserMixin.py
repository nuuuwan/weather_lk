from functools import cached_property
import re

from utils import String, TimeFormat

from weather_lk.REGEX import REGEX


class WeatherReportPDFWeatherListParserMixin:
    def clean_cell(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        return cell

    def clean_row(self, row):
        return [
            WeatherReportPDFWeatherListParserMixin.clean_cell(cell)
            for cell in row
        ]

    def clean_location_name(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        cell = cell.replace('wkqrdOmqrh', '')
        cell = cell.replace('polonnaruwa', 'Polonnaruwa')
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
    def weather_list_ut(self):
        for row in self.table:
            row = self.clean_row(row)
            row_str = ' '.join(row)
            result = re.search(REGEX.DATE, row_str)
            if result:
                date_str = result.groupdict().get('date_str')
                return TimeFormat('%Y.%m.%d').parse(date_str).ut
        return None

    @cached_property
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

    @cached_property
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
                )
            )
        if rain2 is not None:
            weather_list.append(
                dict(
                    place=place2,
                    rain=rain2,
                )
            )
        return weather_list

    @cached_property
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
        return weather_list
