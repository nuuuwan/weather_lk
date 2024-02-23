from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.constants import DIR_DATA_CHARTS_RAINFALL

log = Log('ChartPlaceRainfall')


class ChartPlaceRainfall(ChartPlace):
    def get_dir(self):
        return DIR_DATA_CHARTS_RAINFALL

    def get_data(self):
        x = [
            datetime.strptime(d['date'], '%Y-%m-%d')
            for d in self.data_for_place
        ]
        y_rain = [d['rain'] for d in self.data_for_place]

        # clean nulls
        x, y_rain = zip(*[z for z in zip(x, y_rain) if (z[1] is not None)])

        return x, y_rain

    @staticmethod
    def plot_bars(x, y_rain):
        plt.bar(x, y_rain, color='b', width=1)

    def draw(self):
        x, y_rain = self.get_data()
        self.set_text('Rainfall (mm)')
        plt.ylim([0, 200])
        ChartPlace.annotate(x, y_rain, True, lambda __: 200, 'b', 'mm',10)
        ChartPlaceRainfall.plot_bars(x, y_rain)
