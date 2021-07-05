"""Tests for daily_weather_report."""

import unittest

from weather_lk import _utils


class TestCase(unittest.TestCase):
    """Tests."""

    def test_parse_float(self):
        """Test."""
        self.assertEqual(
            _utils._parse_float('0.1'),
            0.1,
        )


if __name__ == '__main__':
    unittest.main()
