from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import TIME_FORMAT_TIME, Log, Time

from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.constants import DIR_DATA_CHARTS_MIN_MAX_PLOT

log = Log('ChartMinMaxPlot')


class ChartMinMaxPlot(ChartPlace):
    def get_dir(self):
        return DIR_DATA_CHARTS_MIN_MAX_PLOT

    def get_data(self):
        d_list = self.data_for_place

        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in d_list]
        y_min_temp = [d['min_temp'] for d in d_list]
        y_max_temp = [d['max_temp'] for d in d_list]

        # clean nulls
        x, y_min_temp, y_max_temp = zip(
            *[
                z
                for z in zip(x, y_min_temp, y_max_temp)
                if (z[1] is not None)
                and (z[2] is not None)
                and (z[1] <= z[2])
            ]
        )

        return y_min_temp, y_max_temp

    def before_draw(self):
        plt.close()
        fig, ax = plt.subplots()

        fig.autofmt_xdate()
        fig.set_size_inches(12, 12)

        for side in ['bottom', 'left', 'top', 'right']:
            ax.spines[side].set_visible(False)

        ax.grid(True, which='minor', linewidth=0.25, color='#ccc')
        ax.grid(True, which='major', linewidth=0.5, color='#888')

        plt.grid(True)

    def draw(self):
        y_min_temp, y_max_temp = self.get_data()

        plt.scatter(y_min_temp, y_max_temp, color=(1, 0, 0, 0.1), marker='o')

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        self.set_text()

    def set_text(self):
        plt.title(self.get_title(), fontsize=20)
        plt.xlabel('Min Temperature (°C)')
        plt.ylabel('Max Temperature (°C)')

        time_str = TIME_FORMAT_TIME.stringify(Time.now())
        footer_text = f'Generated at {time_str}'
        plt.figtext(0.5, 0.05, footer_text, ha='center', fontsize=8)
