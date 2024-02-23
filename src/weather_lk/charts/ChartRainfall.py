import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import Log

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
    def get_a(y):
        if y > 100:
            return 'f'
        if y > 50:
            return 'c'
        if y > 25:
            return '8'
        return '4'

    @staticmethod
    def get_color(y):
        return '#008' + ChartRainfall.get_a(y)

    @staticmethod
    def plot_bars(x, y_rain):
        bars = plt.bar(x, y_rain, color='b', width=0.9)
        for bar, y in zip(bars, y_rain):
            bar.set_color(ChartRainfall.get_color(y))
