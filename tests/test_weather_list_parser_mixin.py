from unittest import TestCase

from utils import Time, TimeFormat

from tests.test_parser_mixin import TEST_WR


class TestWeatherListParserMixin(TestCase):
    def test_clean_cell(self):
        for [cell, expected_cell] in [
            ['\xa0', ''],
            ['\xa0\xa0', ''],
            ['two  spaces', 'two spaces'],
            [' leading spaces', 'leading spaces'],
            ['training spaces', 'training spaces'],
        ]:
            self.assertEqual(TEST_WR.clean_cell(cell), expected_cell)

    def test_clean_row(self):
        for [row, expected_row] in [
            [
                ['\xa0', 'two  spaces', ' leading spaces', 'training spaces'],
                ['', 'two spaces', 'leading spaces', 'training spaces'],
            ],
        ]:
            self.assertEqual(TEST_WR.clean_row(row), expected_row)

    def test_clean_location_name(self):
        for [name, cleaned_name] in [
            ['\xa0Colombo', 'Colombo'],
            ['Colombo  Fort', 'Colombo Fort'],
            ['polonnaruwa', 'Polonnaruwa'],
            ['wkqrdOmqrh', ''],
        ]:
            self.assertEqual(TEST_WR.clean_location_name(name), cleaned_name)

    def test_weather_list_ut(self):
        ut = TEST_WR.weather_list_ut
        self.assertEqual(ut, 1675276200.0)
        date_id = TimeFormat('%Y-%m-%d').stringify(Time(ut))
        self.assertEqual(date_id, TEST_WR.date_id)

    def test_parse_single_place_row(self):
        self.assertEqual(
            TEST_WR.parse_single_place_row(TEST_WR.table[4]),
            [
                dict(
                    place='Anuradhapura',
                    min_temp=22.7,
                    max_temp=28.6,
                    rain=30.5,
                )
            ],
        )

    def test_parse_double_place_row(self):
        self.assertEqual(
            TEST_WR.parse_double_place_row(TEST_WR.table[30]),
            [
                dict(
                    place='Castlereigh',
                    rain=3.4,
                ),
                dict(
                    place='Randenigala',
                    rain=1.3,
                ),
            ],
        )

    def test_parse_row(self):
        self.assertEqual(
            TEST_WR.parse_row(TEST_WR.table[1]),
            [],
        )

        self.assertEqual(
            TEST_WR.parse_row(TEST_WR.table[4]),
            TEST_WR.parse_single_place_row(TEST_WR.table[4]),
        )
        self.assertEqual(
            TEST_WR.parse_row(TEST_WR.table[30]),
            TEST_WR.parse_double_place_row(TEST_WR.table[30]),
        )

    def test_weather_list(self):
        self.assertEqual(
            len(TEST_WR.weather_list),
            57,
        )
