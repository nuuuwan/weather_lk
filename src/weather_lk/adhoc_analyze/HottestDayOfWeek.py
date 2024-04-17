import datetime
import math
import os

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.core import Data

log = Log('HottestDayOfWeek')
DAYS_OF_WEEK = [
    '1-Mon',
    '2-Tue',
    '3-Wed',
    '4-Thu',
    '5-Fri',
    '6-Sat',
    '7-Sun',
]
Q = 0.1


class HottestDayOfWeek:
    def __init__(self, place):
        self.place = place

    @property
    def data(self):
        idx_by_place = Data.idx_by_place()
        return idx_by_place.get(self.place, None)

    @property
    def day_of_week_to_data(self):
        day_of_week_to_data = {}
        for data in self.data:
            date_str = data['date']
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            day_of_week = dt.weekday()
            day_of_week_str = DAYS_OF_WEEK[day_of_week]
            if day_of_week_str not in day_of_week_to_data:
                day_of_week_to_data[day_of_week_str] = []
            day_of_week_to_data[day_of_week_str].append(data)
        return day_of_week_to_data

    @staticmethod
    def summary_statistics_for_dim(x_list):
        n = len(x_list)
        if n == 0:
            return None
        x_list.sort()
        mean = sum(x_list) / n
        stdev = (sum([(x - sum(x_list) / n) ** 2 for x in x_list]) / n) ** 0.5
        return dict(
            min=x_list[0],
            max=x_list[-1],
            mean=mean,
            stdev=stdev,
            mean_plus2=mean + 2 * stdev,
            mean_minus2=mean - 2 * stdev,
            median=x_list[n // 2],
            q1=x_list[n // 4],
            q3=x_list[3 * n // 4],
            n=n,
        )

    @staticmethod
    def summary_statistics(day_of_week, data_list):
        data_list_with_temp = [
            data
            for data in data_list
            if data.get('min_temp') and data.get('max_temp')
        ]
        n = len(data_list_with_temp)

        min_temp_list = [data['min_temp'] for data in data_list_with_temp]
        max_temp_list = [data['max_temp'] for data in data_list_with_temp]
        mean_temp_list = [
            (min_temp + max_temp) / 2.0
            for min_temp, max_temp in zip(min_temp_list, max_temp_list)
        ]

        return dict(
            n=n,
            mean_temp=HottestDayOfWeek.summary_statistics_for_dim(
                mean_temp_list
            ),
            min_temp=HottestDayOfWeek.summary_statistics_for_dim(
                min_temp_list
            ),
            max_temp=HottestDayOfWeek.summary_statistics_for_dim(
                max_temp_list
            ),
        )

    @property
    def day_of_week_to_summary_statistics(self):
        return {
            day_of_week: HottestDayOfWeek.summary_statistics(
                day_of_week, data_list
            )
            for day_of_week, data_list in self.day_of_week_to_data.items()
        }

    def draw_chart_range(self):
        stats = self.day_of_week_to_summary_statistics

        x = DAYS_OF_WEEK
        y_temp_min_mean = [
            stats[dow]['mean_temp']['mean_minus2'] for dow in x
        ]
        y_temp_max_mean = [stats[dow]['mean_temp']['mean_plus2'] for dow in x]
        y_temp_diff = [
            y_max - y_min
            for y_max, y_min in zip(y_temp_max_mean, y_temp_min_mean)
        ]
        y = [stats[dow]['mean_temp']['mean'] for dow in x]

        plt.close()
        plt.bar(x, y_temp_min_mean, color="white")
        plt.bar(x, y_temp_diff, color="pink", bottom=y_temp_min_mean)
        plt.plot(x, y, color="red")

        plt.title(
            f'{self.place} - Max and Min Daily Temp - Mean across Days of Week'
        )
        plt.xlabel('Day of Week')
        plt.ylabel('Temperature (Celsius)')

        ylim_min = math.floor(min(y_temp_min_mean) / Q) * Q
        ylim_max = math.ceil(max(y_temp_max_mean) / Q) * Q
        plt.ylim(ylim_min, ylim_max)

        image_path = os.path.join(
            'src',
            'weather_lk',
            'adhoc_analyze',
            f'HottestDayOfWeek.range.{self.place}.png',
        )
        plt.savefig(image_path)
        plt.close()
        log.info(f'Saved {image_path}')
        os.startfile(image_path)

    def draw_chart_line(self):
        stats = self.day_of_week_to_summary_statistics
        x = DAYS_OF_WEEK
        y = [stats[dow]['mean_temp']['mean'] for dow in x]
        ylim_min = math.floor(min(y) / Q) * Q
        ylim_max = math.ceil(max(y) / Q) * Q

        plt.close()
        plt.plot(x, y, color="red")

        plt.title(
            f'{self.place} - Mean Daily Temp - Mean across Days of Week'
        )
        plt.xlabel('Day of Week')
        plt.ylabel('Temperature (Celsius)')
        plt.ylim(ylim_min, ylim_max)

        image_path = os.path.join(
            'src',
            'weather_lk',
            'adhoc_analyze',
            f'HottestDayOfWeek.line.{self.place}.png',
        )
        plt.savefig(image_path)
        plt.close()
        log.info(f'Saved {image_path}')
        os.startfile(image_path)


def main():
    for place in ['Colombo', 'Katugastota', 'Jaffna', 'Galle']:
        h = HottestDayOfWeek(place)
        h.draw_chart_line()
        h.draw_chart_range()


if __name__ == "__main__":
    main()
