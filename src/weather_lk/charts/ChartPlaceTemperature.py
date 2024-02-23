from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.constants import (DIR_DATA_CHARTS_TEMPERATURE,
                                  LIMIT_AND_COLOR_LIST)

log = Log('ChartPlaceTemperature')


class ChartPlaceTemperature(ChartPlace):
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
    def set_ylim(y_min, y_max):
        min_temp = min(y_min) - 1
        max_temp = max(y_max) + 1
        plt.ylim([min_temp, max_temp])

    @staticmethod
    def plot_bars(x, y_min_temp, y_max_temp):
        for [limit, color] in LIMIT_AND_COLOR_LIST:
            q = list(
                zip(
                    *[
                        z
                        for z in zip(x, y_max_temp)
                        if (limit <= z[1] < limit + 5)
                    ]
                )
            )
            if not q:
                continue
            x2, y_max_temp2 = q
            plt.bar(
                x2,
                y_max_temp2,
                color=color,
                width=1,
            )

        plt.bar(x, y_min_temp, color='w', width=1)

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
        ChartPlace.annotate(x, y_max_temp, True, max, 'r', '°C')
        ChartPlace.annotate(x, y_min_temp, False, min, 'b', '°C')
        ChartPlaceTemperature.plot_bars(x, y_min_temp, y_max_temp)
        ChartPlaceTemperature.plot_rolling(x, y_min_temp, y_max_temp)
