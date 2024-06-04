from datetime import datetime

from matplotlib import pyplot as plt
from utils import Log

from weather_lk.charts.Chart import Chart
from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.charts.ChartRainfall import ChartRainfall
from weather_lk.core import Data

log = Log('ChartPlaceRainfall')


class ChartPlaceRainfall(ChartPlace, ChartRainfall):
    def get_dir(self):
        return Data.DIR_DATA_CHARTS_RAINFALL

    def get_data(self):
        d_list = self.data_for_place
        if self.window:
            d_list = d_list[-self.window:]
        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in d_list]
        y_rain = [d['rain'] for d in d_list]

        # clean nulls
        x, y_rain = zip(*[z for z in zip(x, y_rain) if (z[1] is not None)])

        return x, y_rain

    @staticmethod
    def plot_rolling(x, y_rain):
        window = Chart.ROLLING_WINDOW
        y_rain_rolling = [
            sum(y_rain[i - window + 1: i + 1]) / window
            for i in range(window, len(y_rain))
        ]
        x_rolling = x[window:]
        plt.plot(
            x_rolling,
            y_rain_rolling,
            color='black',
            linewidth=0.5,
            label=f"{window}-day rolling average",
        )
        plt.legend()

    def draw(self):
        x, y_rain = self.get_data()
        self.set_text('Rainfall (mm)')
        ylim = self.set_ylim(y_rain)

        ChartPlaceRainfall.annotate(
            x, y_rain, True, lambda __: ylim - 25, '#008', 'mm', 25
        )
        ChartPlaceRainfall.plot_bars(x, y_rain)
        ChartPlaceRainfall.plot_rolling(x, y_rain)
