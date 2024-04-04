import os
from datetime import datetime

import matplotlib.pyplot as plt
from utils import TimeUnit, TimeFormat, Log, Time, TSVFile

from weather_lk.core.Data import Data

log = Log('SummaryCoverage')


class SummaryCoverage:
    COVERAGE_WINDOW_LIST = [7, 28, 365, 3652]

    @staticmethod
    def get_n_temp(weather_list):
        return sum(
            1
            for w in weather_list
            if w.get('max_temp', w.get('max_temp', None)) is not None
        )

    @staticmethod
    def get_n_rain(weather_list):
        return sum(1 for w in weather_list if (w['rain'] is not None))

    def get_coverage(self):
        t = Time.now()
        idx_by_date = Data.idx_by_date()
        c_list = []
        max_days = max(SummaryCoverage.COVERAGE_WINDOW_LIST)
        for i in range(0, max_days):
            date = TimeFormat.DATE.stringify(
                Time(t.ut - TimeUnit.SECONDS_IN.DAY * i + 1)
            )
            n, n_temp, n_rain = 0, 0, 0
            has_data = date in idx_by_date
            if has_data:
                data_for_date = idx_by_date[date]
                weather_list = data_for_date['weather_list']
                n = len(weather_list)
                n_temp = SummaryCoverage.get_n_temp(weather_list)
                n_rain = SummaryCoverage.get_n_rain(weather_list)

            c_list.append(
                dict(
                    date=date,
                    has_data=has_data,
                    n=n,
                    n_temp=n_temp,
                    n_rain=n_rain,
                )
            )
        return c_list

    def write_coverage(self):
        coverage = self.get_coverage()
        tsv_path = os.path.join(Data.DIR_REPO, 'coverage.tsv')
        TSVFile(tsv_path).write(coverage)
        log.info(f'Wrote coverage to {tsv_path}')

        for window in SummaryCoverage.COVERAGE_WINDOW_LIST:
            self.draw_coverage_chart(window)

    def draw_coverage_chart(self, window):
        coverage = self.get_coverage()[:window]
        x = [datetime.strptime(c['date'], '%Y-%m-%d') for c in coverage]
        y_rain = [c['n_rain'] for c in coverage]
        y_temp = [c['n_temp'] for c in coverage]

        n_total = len(coverage)
        n_with_data = sum(
            1 for c in coverage if c['n_rain'] > 0 or c['n_temp'] > 0
        )
        title = f'{n_with_data:,} of the last {n_total:,} days have data'

        plt.close()
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Number of Places Covered')

        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        plt.bar(x, y_rain, color='b', label='Rainfall')
        plt.bar(x, y_temp, color='r', label='Temperature & Rainfall')
        plt.legend(loc='upper left')

        image_path = os.path.join(Data.DIR_REPO, f'coverage-{window}days.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')

