"""Tests for daily_weather_report."""

import unittest

from weather_lk import daily_weather_report


class TestDailyWeatherReport(unittest.TestCase):
    """Tests."""

    def test_daily_weather_report(self):
        """Test."""
        self.assertTrue(daily_weather_report.daily_weather_report())


if __name__ == '__main__':
    unittest.main()
