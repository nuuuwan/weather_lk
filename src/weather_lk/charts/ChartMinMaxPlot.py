from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from utils import TIME_FORMAT_TIME, Log, Time

from weather_lk.charts.ChartPlace import ChartPlace
from weather_lk.charts.ChartTemperature import ChartTemperature
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

        return x, y_min_temp, y_max_temp

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
        __, y_min_temp, y_max_temp = self.get_data()
        n = len(y_min_temp)
        for i, (x_i, y_i) in enumerate(zip(y_min_temp, y_max_temp)):
            mid_temp = (x_i + y_i) / 2
            color = ChartTemperature.get_color(mid_temp)
            if i >= n - 28:
                edgecolors = "#000"
            elif i >= n - 91:
                edgecolors = "#888"
            else:
                edgecolors = "#ccc"
            plt.scatter(
                x_i, y_i, color=color, edgecolors=edgecolors, marker='o'
            )

        self.draw_lines()
        self.annotate()

    def draw_lines(self):
        ax = plt.gca()
        
        x_lim = ax.get_xlim()
        y_lim = ax.get_ylim()

        __, y_min_temp, y_max_temp = self.get_data()

        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        # x=y
        min_min_temp = np.min(y_min_temp)
        max_max_temp = np.max(y_max_temp)
        d_max = int(max_max_temp - min_min_temp )
        min_max_temp = np.max(y_min_temp)
        max_min_temp = np.min(y_max_temp)

        for d in range(0, d_max):
            lims = [
                min_max_temp,
                min(max_min_temp - d, min_max_temp),
            ]
            lims2 = [
                max(min_max_temp + d, max_min_temp),
                max_min_temp,
            ]
            if d % 5 == 0:
                color = '#cccf'
            else:
                color = '#ccc2'
            ax.plot(lims, lims2, color=color, linestyle='--')

        # min-median
        min_median = np.median(y_min_temp)
        plt.axvline(x=min_median, color='#0088', linestyle='--')

        # max-median
        max_median = np.median(y_max_temp)
        plt.axhline(y=max_median, color='#8008', linestyle='--')

        # text
        self.set_text()

        # force lims
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)

    def annotate(self):
        x, y_min_temp, y_max_temp = self.get_data()
        candidate_y_min = sorted(y_min_temp)[:3]
        candidate_y_max = sorted(y_max_temp)[-3:]

        for x_i, y_min_i, y_max_i in zip(x, y_min_temp, y_max_temp):
            if (y_min_i in candidate_y_min):
                color = ChartTemperature.get_color(y_min_i)
                color_light = color + (0.25,)
                date_str = x_i.strftime('%Y-%m-%d')
                caption = f'{date_str} {y_min_i:.1f}°C'
                plt.annotate(
                    xy=(y_min_i, y_max_i),
                    xytext=(y_min_i, y_max_i),
                    text=caption,
                    color=color,
                    bbox=dict(
                        facecolor=color_light, edgecolor='none', boxstyle="round"
                    ),
                )
            if (y_max_i in candidate_y_max):
                color = ChartTemperature.get_color(y_max_i)
                color_light = color + (0.25,)
                date_str = x_i.strftime('%Y-%m-%d')
                caption = f'{date_str} {y_max_i:.1f}°C'
                plt.annotate(
                    xy=(y_min_i, y_max_i),
                    xytext=(y_min_i, y_max_i),
                    text=caption,
                    color=color,
                    bbox=dict(
                        facecolor=color_light, edgecolor='none', boxstyle="round"
                    ),
                )

   

    def set_text(self):
        plt.title(self.get_title(), fontsize=20)
        plt.xlabel('Min Temperature (°C)')
        plt.ylabel('Max Temperature (°C)')

        time_str = TIME_FORMAT_TIME.stringify(Time.now())
        footer_text = f'Generated at {time_str}'
        plt.figtext(0.5, 0.05, footer_text, ha='center', fontsize=8)
