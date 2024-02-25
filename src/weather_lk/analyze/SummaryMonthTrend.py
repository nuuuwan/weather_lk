from functools import cached_property

import matplotlib.colors as colors

from utils_future.Markdown import Markdown
from weather_lk.charts.ChartRainfall import ChartRainfall
from weather_lk.charts.ChartTemperature import ChartTemperature
from weather_lk.core.Data import Data

MONTH_NAMES = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec',
}


class SummaryMonthTrend:
    def __init__(self, place):
        self.place = place

    @cached_property
    def data(self):
        idx = Data.idx_by_place()
        return idx[self.place]

    @cached_property
    def month_to_data(self):
        idx = {}
        for d in self.data:
            date = d['date']
            month = date[5:7]
            if month not in idx:
                idx[month] = []
            idx[month].append(d)

        return {
            month: data
            for month, data in sorted(idx.items(), key=lambda x: x[0])
        }

    @staticmethod
    def get_month_stats(data_for_month):
        n = len(data_for_month)
        min_temp_list = [d['min_temp'] for d in data_for_month]
        max_temp_list = [d['max_temp'] for d in data_for_month]
        rain_list = [d['rain'] for d in data_for_month]

        mid_temp_list = [
            (min_temp_list[i] + max_temp_list[i]) / 2
            for i in range(n)
            if min_temp_list[i] and max_temp_list[i]
        ]
        min_temp_list = [t for t in min_temp_list if t]
        max_temp_list = [t for t in max_temp_list if t]

        min_temp = min(min_temp_list)
        max_temp = max(max_temp_list)
        avg_min_temp = sum(min_temp_list) / n
        avg_max_temp = sum(max_temp_list) / n
        avg_mid_temp = sum(mid_temp_list) / n

        avg_rain = sum(rain_list) / n
        p_days_rain = len([d for d in rain_list if d > 0]) / n

        return dict(
            n=n,
            max_temp=max_temp,
            avg_max_temp=avg_max_temp,
            avg_mid_temp=avg_mid_temp,
            avg_min_temp=avg_min_temp,
            min_temp=min_temp,
            avg_rain=avg_rain,
            p_days_rain=p_days_rain,
        )

    @cached_property
    def month_to_stats(self):
        return {
            month: self.get_month_stats(data)
            for month, data in self.month_to_data.items()
        }

    @staticmethod
    def format_stat(stat, stat_key):
        if 'temp' in stat_key:
            (r, g, b) = ChartTemperature.get_color(stat)
            hex_color = colors.rgb2hex((r, g, b))
            return f'$$\\color{{{hex_color}}}{stat:.1f}$$'
        if 'rain' in stat_key:
            (r, g, b,__) = ChartRainfall.get_color(stat)
            hex_color = colors.rgb2hex((r, g, b))
            return f'$$\\color{{{hex_color}}}{stat:.1%}$$'
        if 'p_' in stat_key:
            (r, g, b) = ChartTemperature.get_color(stat * 30 + 5)
            hex_color = colors.rgb2hex((r, g, b))
            return f'$$\\color{{{hex_color}}}{stat:.1%}$$'

        if stat_key == 'n':
            return f'{stat:,}'
        return f'{stat:.1f}'

    @staticmethod
    def format_stat_key(stat_key):
        return {
            'n': 'Sample Size (Days)',
            'max_temp': 'Record High (°C)',
            'avg_max_temp': 'Mean daily maximum (°C)',
            'avg_mid_temp': 'Daily Mean (°C)',
            'avg_min_temp': 'Mean daily minimum (°C)',
            'min_temp': 'Record Low (°C)',
            'avg_rain': 'Avg Rain (mm)',
            'p_days_rain': '% Days Rain',
        }.get(stat_key, stat_key)

    @cached_property
    def md_table(self):
        month_to_stats = self.month_to_stats
        months = list(month_to_stats.keys())
        lines = [f'## {self.place}', '']
        keys = ['Stat'] + [MONTH_NAMES[month] for month in months]
        values_list = []
        stat_keys = list(month_to_stats.values())[0].keys()
        for stat_key in stat_keys:
            values = []
            for month in months:
                stats = month_to_stats[month]
                stat = stats[stat_key]
                value = SummaryMonthTrend.format_stat(stat, stat_key)
                values.append(value)
            stat_key_value = SummaryMonthTrend.format_stat_key(stat_key)
            values_list.append([stat_key_value] + values)
        lines.extend(Markdown.build_table(keys, values_list))
        lines.append('')
        return lines
