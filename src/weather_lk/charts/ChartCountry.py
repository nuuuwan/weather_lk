from functools import cached_property

from weather_lk.charts.Chart import Chart
from weather_lk.core.Data import Data


class ChartCountry(Chart):
    def __init__(self):
        self.data_latest = Data.max()
        self.window = None

    def get_xlabel(self):
        return ''

    @cached_property
    def sorted_weather_list(self):
        return sorted(
            self.data_latest['weather_list'],
            key=lambda x: x['lng'],
        )
