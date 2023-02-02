from unittest import TestCase, skip

from utils import get_date_id

from weather_lk import WeatherReport

TEST_WR = WeatherReport()


class TestWRDownloader(TestCase):
    def test_date_id(self):
        self.assertEqual(TEST_WR.date_id, get_date_id())

    def test_file_path(self):
        date_id = get_date_id()
        self.assertEqual(TEST_WR.file_path, f'/tmp/weather_lk.{date_id}.pdf')

    @skip('slow')
    def test_download(self):
        if TEST_WR.file.exists:
            TEST_WR.file.remove()
        TEST_WR.download()
