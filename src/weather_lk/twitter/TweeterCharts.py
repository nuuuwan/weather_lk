"""Tweet."""
import math
import os

from infograph import BarChart, DataTable, Infograph, RangeBarChart

from weather_lk.constants import DIR_REPO_DAILY_DATA


def func_color_rain(_, yi):
    b = 1
    r = 0
    for limit, x in [
        [100, 1],
        [50, 2],
        [25, 3],
        [-1, 4],
    ]:
        if yi > limit:
            a = math.sqrt(1.0 / x)
            g = 1 - a / 2
            break

    return (r, g, b, a)


def func_color_temp(_, __, y2i):
    a = 0.5
    for limit, color in [
        [35, (0.5, 0, 0, a)],
        [30, (1, 0, 0, a)],
        [25, (1, 0.5, 0, a)],
        [20, (0, 1, 0, a)],
        [15, (0, 0.5, 1, a)],
        [10, (0, 0, 1, a)],
    ]:
        if y2i > limit:
            return color
    return (0, 0, 0.5, a)


class TweeterCharts:
    @property
    def tweet_image_path(self):
        return os.path.join(
            DIR_REPO_DAILY_DATA,
            f'weather_lk.{self.weather_report.date_id}.png',
        )

    def get_temp_chart(self):
        data_table = DataTable(
            [
                d
                for d in self.weather_report.weather_list
                if d['rain'] is not None
            ],
        )
        data_table.sort('lng')
        return BarChart(
            'Rainfall (mm)',
            data_table['place'],
            data_table['rain'],
            func_color_rain,
        )

    def get_rain_chart(self):
        data_table = DataTable(
            [
                d
                for d in self.weather_report.weather_list
                if d['min_temp'] is not None and d['max_temp'] is not None
            ],
        )
        data_table.sort('lng')
        return RangeBarChart(
            'Temperature (°C)',
            data_table['place'],
            data_table['min_temp'],
            data_table['max_temp'],
            func_color_temp,
        )

    def build_tweet_image(self):
        infograph = Infograph(
            'Sri Lanka',
            'Temperature & Rainfall',
            self.weather_report.weather_data['date'],
            'meteo.gov.lk',
        )

        infograph.add(self.get_temp_chart())
        infograph.add(self.get_rain_chart())
        infograph.write(self.tweet_image_path)
