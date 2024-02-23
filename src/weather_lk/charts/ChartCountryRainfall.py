import os

import matplotlib.pyplot as plt

from weather_lk.charts.Chart import Chart
from weather_lk.charts.ChartCountry import ChartCountry
from weather_lk.charts.ChartRainfall import ChartRainfall
from weather_lk.constants import DIR_DATA_CHARTS


class ChartCountryRainfall(ChartCountry, ChartRainfall):
    def get_label(self):
        return 'country_rainfall'

    def get_dir(self):
        return DIR_DATA_CHARTS

    def get_data(self):
        sorted_weather_list = self.sorted_weather_list
        x = [d['place'] for d in sorted_weather_list]
        y_rain = [d['rain'] for d in sorted_weather_list]

        # clean nulls
        x, y_rain = zip(*[z for z in zip(x, y_rain) if (z[1] is not None)])

        return x, y_rain

    def get_title(self):
        date = self.data_latest['date']
        return f'Rainfall ({date})'

    def draw(self):
        self.set_text('Rainfall (mm)')
        x, y_rain = self.get_data()
        self.set_ylim()
        plt.tick_params(axis='x', labelsize=5)
        ChartRainfall.plot_bars(x, y_rain)
        Chart.annotate(x, y_rain, True, lambda __: 175, '#008', 'mm', 25)


if __name__ == '__main__':
    image_path = ChartCountryRainfall().write()
    os.startfile(image_path)
