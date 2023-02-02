from unittest import TestCase

from weather_lk import WeatherReport


class MockHackWeatherReport(WeatherReport):
    @property
    def file_path(self):
        return 'tests/data.pdf'


TEST_WR = MockHackWeatherReport()


class TestParserMixin(TestCase):
    def test_table(self):
        self.assertEqual(len(TEST_WR.table), 53)
