import colorsys
import math

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import Log

log = Log('ChartTemperature')


class ChartTemperature:
    @staticmethod
    def set_ylim(y_min, y_max):
        Q = 5
        G = 2
        min_temp = math.ceil(min(y_min) / Q - G) * Q
        max_temp = math.floor(max(y_max) / Q + G) * Q

        plt.ylim([min_temp, max_temp])

        ax = plt.gca()
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

    @staticmethod
    def get_color(y):
        MIN_TEMP, MAX_TEMP = 15, 30
        MIN_H, MAX_H = 0, 240
        y = max(min(MAX_TEMP, y), MIN_TEMP)
        p = 1 - (y - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)
        h = (MIN_H + p * (MAX_H - MIN_H)) / 360.0
        s = 1
        l = 0.5
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        a = 0.5
        return (r, g, b, a)

    @staticmethod
    def plot_bars(x, y_min_temp, y_max_temp):
        width = 0.9
        y_mid_temp = [(a + b) / 2 for a, b in zip(y_min_temp, y_max_temp)]

        bars = plt.bar(x, y_max_temp, color='w', edgecolor='w', width=width)
        for bar, y in zip(bars, y_mid_temp):
            bar.set_color(ChartTemperature.get_color(y))

        bars = plt.bar(x, y_min_temp, edgecolor='w', color='w', width=width)
        for bars in bars:
            bars.set_color('w')
