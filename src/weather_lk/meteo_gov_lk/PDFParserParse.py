import re
from functools import cached_property

import camelot
from utils import Log, String

from weather_lk.meteo_gov_lk.REGEX import REGEX

log = Log('PDFParserParse')


class PDFParserParse:
    @cached_property
    def table(self):
        tables = camelot.read_pdf(self.pdf_path, pages='all')
        table = tables[0].df.values.tolist()
        return table

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
