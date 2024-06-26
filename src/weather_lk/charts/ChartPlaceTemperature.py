from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.charts.Chart import Chart
from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.charts.ChartTemperature import ChartTemperature
from weather_lk.core import Data

log = Log('ChartPlaceTemperature')


class ChartPlaceTemperature(ChartPlace, ChartTemperature):
    def get_dir(self):
        return Data.DIR_DATA_CHARTS_TEMPERATURE

    def get_data(self):
        d_list = self.data_for_place
        if self.window:
            d_list = d_list[-self.window:]

        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in d_list]
        y_min_temp = [d['min_temp'] for d in d_list]
        y_max_temp = [d['max_temp'] for d in d_list]

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
        window = Chart.ROLLING_WINDOW
        y_temp_mid_rolling = [
            sum(y_temp_mid[i - window: i]) / window
            for i in range(window, len(y_temp_mid))
        ]
        x_rolling = x[window:]
        plt.plot(
            x_rolling,
            y_temp_mid_rolling,
            color='black',
            linewidth=0.5,
            label=f"{window}-day rolling average",
        )
        plt.legend()

    def draw(self):
        x, y_min_temp, y_max_temp = self.get_data()
        self.set_ylim(y_min_temp, y_max_temp)
        self.set_text('Temperature (°C)')
        ChartPlaceTemperature.set_ylim(y_min_temp, y_max_temp)
        ChartPlaceTemperature.annotate(
            x, y_max_temp, True, max, '#c00', '°C', 2
        )
        ChartPlaceTemperature.annotate(
            x, y_min_temp, False, min, '#008', '°C', 2
        )
        ChartPlaceTemperature.plot_bars(x, y_min_temp, y_max_temp)
        ChartPlaceTemperature.plot_rolling(x, y_min_temp, y_max_temp)
