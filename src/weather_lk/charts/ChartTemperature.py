import math

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import Log

from weather_lk.constants import LIMIT_AND_COLOR_LIST, MIN_COLOR

log = Log('ChartTemperature')


class ChartTemperature:
    @staticmethod
    def set_ylim(y_min, y_max):
        Q = 5
        min_temp = math.ceil(min(y_min) / Q - 1) * Q
        max_temp = math.floor(max(y_max) / Q + 1) * Q

        plt.ylim([min_temp, max_temp])

        ax = plt.gca()
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

    @staticmethod
    def get_color(y):
        for limit, color in LIMIT_AND_COLOR_LIST:
            if y >= limit:
                return color
        return MIN_COLOR

    @staticmethod
    def plot_bars(x, y_min_temp, y_max_temp):
        width = 0.9
        bars = plt.bar(x, y_max_temp, color='w', width=width)
        for bar, y in zip(bars, y_max_temp):
            bar.set_color(ChartTemperature.get_color(y))
        bars = plt.bar(x, y_min_temp, color='w', width=width)
        for bars in bars:
            bars.set_color('w')
