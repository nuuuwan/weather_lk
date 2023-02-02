from unittest import TestCase

from weather_lk import WeatherReport


class MockHackWeatherReport(WeatherReport):
    @property
    def file_path(self):
        return 'tests/data.pdf'

    @property
    def date_id(self):
        return '2023-02-02'


TEST_WR = MockHackWeatherReport()


class TestParserMixin(TestCase):
    def test_table(self):
        self.assertEqual(len(TEST_WR.table), 53)
