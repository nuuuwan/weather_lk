import os
from unittest import TestCase

from tests.test_parser_mixin import TEST_WR


class TestLoaderMixin(TestCase):
    def test_remote_weather_data_url(self):
        self.assertEqual(
            TEST_WR.remote_weather_data_url,
            os.path.join(
                'https://raw.githubusercontent.com',
                'nuuuwan',
                'weather_lk',
                'data',
                'weather_lk.2023-02-02.json',
            ),
        )

    def test_load_local(self):
        self.assertEqual(
            TEST_WR.load_local(),
            TEST_WR.weather_data,
        )

    def test_load(self):
        self.assertEqual(
            TEST_WR.load(),
            TEST_WR.weather_data,
        )
