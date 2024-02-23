import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import Log
import colorsys

log = Log('ChartRainfall')


class ChartRainfall:
    @staticmethod
    def set_ylim(y_rain):
        max_y = max(y_rain)
        ylim = max(200, max_y + 50)
        plt.ylim([0, ylim])

        ax = plt.gca()
        ax.yaxis.set_major_locator(MultipleLocator(25))
        ax.yaxis.set_minor_locator(MultipleLocator(5))

        return ylim

    @staticmethod
    def get_color(y):
        y = max(min(200, y), 0)
        p = y / 200.0
        h = (120 + 120 * p) / 360.0
        s = 1
        l = 0.5
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        a = 0.5
        return (r, g, b, a)

    @staticmethod
    def plot_bars(x, y_rain):
        bars = plt.bar(x, y_rain, color='b', width=0.9)
        for bar, y in zip(bars, y_rain):
            bar.set_color(ChartRainfall.get_color(y))
