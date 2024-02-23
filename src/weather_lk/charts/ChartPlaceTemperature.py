from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.charts.ChartPlace import ChartPlace
from    weather_lk.charts.ChartTemperature import ChartTemperature
from weather_lk.constants import (
    DIR_DATA_CHARTS_TEMPERATURE,
    LIMIT_AND_COLOR_LIST,
)


log = Log('ChartPlaceTemperature')


class ChartPlaceTemperature(ChartPlace, ChartTemperature):
    def get_dir(self):
        return DIR_DATA_CHARTS_TEMPERATURE

    def get_data(self):
        x = [
            datetime.strptime(d['date'], '%Y-%m-%d')
            for d in self.data_for_place
        ]
        y_min_temp = [d['min_temp'] for d in self.data_for_place]
        y_max_temp = [d['max_temp'] for d in self.data_for_place]

        # clean nulls
        x, y_min_temp, y_max_temp = zip(
            *[
                z
                for z in zip(x, y_min_temp, y_max_temp)
                if (z[1] is not None) and (z[2] is not None)
            ]
        )

        return x, y_min_temp, y_max_temp



    @staticmethod
    def plot_rolling(x, y_min_temp, y_max_temp):
        y_temp_mid = [(a + b) / 2 for a, b in zip(y_min_temp, y_max_temp)]
        window = 7
        y_temp_mid_rolling = [
            sum(y_temp_mid[i: i + window]) / window
            for i in range(len(y_temp_mid) - window + 1)
        ]
        x_rolling = x[: -(window - 1)]
        plt.plot(x_rolling, y_temp_mid_rolling, color='black')

    def draw(self):
        x, y_min_temp, y_max_temp = self.get_data()

        self.set_text('Temperature (°C)')
        ChartPlaceTemperature.set_ylim(y_min_temp, y_max_temp)
        ChartPlace.annotate(x, y_max_temp, True, max, 'r', '°C', 1)
        ChartPlace.annotate(x, y_min_temp, False, min, 'b', '°C', 1)
        ChartPlaceTemperature.plot_bars(x, y_min_temp, y_max_temp)
        ChartPlaceTemperature.plot_rolling(x, y_min_temp, y_max_temp)
