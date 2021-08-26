"""Tests for daily_weather_report."""

import unittest

from weather_lk import daily_weather_report


class TestCase(unittest.TestCase):
    """Tests."""

    def test_parse_float(self):
        """Test."""
        self.assertEqual(
            daily_weather_report.parse_float('0.1'),
            0.1,
        )


if __name__ == '__main__':
    unittest.main()
