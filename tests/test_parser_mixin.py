from unittest import TestCase

from weather_lk import WeatherReport

TEST_WR = WeatherReport()


class TestParserMixin(TestCase):
    def table_file_path(self):
        return TEST_WR.file_path[:-4] + '.csv'

    def test_table(self):
        self.assertEqual(len(TEST_WR.table), 53)
