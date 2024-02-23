import os
from datetime import datetime

import matplotlib.pyplot as plt
from utils import SECONDS_IN, TIME_FORMAT_DATE, Log, Time, TSVFile

from weather_lk.constants import DIR_REPO
from weather_lk.core.Data import Data

log = Log('SummaryCoverage')


class SummaryCoverage:
    def coverage(self):
        t = Time.now()
        idx_by_date = Data.idx_by_date()
        c_list = []
        for i in range(0, 1000):
            t_i = Time(t.ut - SECONDS_IN.DAY * i + 1)
            date = TIME_FORMAT_DATE.stringify(t_i)
            has_data = date in idx_by_date
            if has_data:
                data_for_date = idx_by_date[date]
                weather_list = data_for_date['weather_list']
                n = len(weather_list)
                n_temp = sum(
                    1
                    for w in weather_list
                    if w.get('max_temp', w.get('max_temp', None)) is not None
                )
                n_rain = sum(
                    1 for w in weather_list if (w['rain'] is not None)
                )
            else:
                n = 0
                n_temp = 0
                n_rain = 0
            c = dict(
                date=date,
                has_data=has_data,
                n=n,
                n_temp=n_temp,
                n_rain=n_rain,
            )
            c_list.append(c)
        return c_list

    def write_coverage(self):
        coverage = self.coverage()
        tsv_path = os.path.join(DIR_REPO, 'coverage.tsv')
        TSVFile(tsv_path).write(coverage)
        log.info(f'Wrote coverage to {tsv_path}')

        self.draw_coverage_chart(window=10)
        self.draw_coverage_chart(window=100)
        self.draw_coverage_chart(window=1000)

    def draw_coverage_chart(self, window):
        coverage = self.coverage()[:window]
        x = [datetime.strptime(c['date'], '%Y-%m-%d') for c in coverage]
        y_rain = [c['n_rain'] for c in coverage]
        y_temp = [c['n_temp'] for c in coverage]

        plt.close()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        plt.title(f'Coverage (Last {window} Days)')
        plt.xlabel('Date')
        plt.ylabel('Number of Places Covered')

        plt.bar(x, y_rain, color='b', label='Rainfall')
        plt.bar(x, y_temp, color='r', label='Temperature & Rainfall')
        plt.legend(loc='upper left')

        image_path = os.path.join(DIR_REPO, f'coverage-{window}days.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')
        # os.startfile(image_path)
