"""Tests for weather_lk."""

import unittest

from weather_lk import run_weather_lk


class TestCase(unittest.TestCase):
    """Tests."""

    def test_run_weather_lk(self):
        """Test."""
        self.assertTrue(run_weather_lk.run_weather_lk())


if __name__ == '__main__':
    unittest.main()
