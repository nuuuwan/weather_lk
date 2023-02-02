from unittest import TestCase

from utils import JSONFile

from tests.test_parser_mixin import TEST_WR


class TestWeatherDataParserMixin(TestCase):
    def test_weather_data_file_path(self):
        self.assertEqual(
            TEST_WR.weather_data_file_path,
            'tests/data.json',
        )

    def test_min_temp(self):
        self.assertEqual(
            TEST_WR.min_temp,
            dict(
                min_temp=14.0,
                min_temp_place='Nuwara Eliya',
            ),
        )

    def test_max_temp(self):
        self.assertEqual(
            TEST_WR.max_temp,
            dict(
                max_temp=31.7,
                max_temp_place='Pothuvil',
            ),
        )

    def test_max_rain(self):
        self.assertEqual(
            TEST_WR.max_rain,
            dict(
                max_rain=150.0,
                max_rain_place='Nedunkerni',
            ),
        )

    def test_weather_data(self):
        self.assertEqual(
            TEST_WR.weather_data,
            JSONFile('tests/data.expected.json').read(),
        )
