import os
from datetime import datetime

import matplotlib.pyplot as plt
from utils import Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import (DIR_DATA_CHARTS, DIR_DATA_CHARTS_RAINFALL,
                                  DIR_DATA_CHARTS_TEMPERATURE, DISPLAY_PLACES,
                                  LIMIT_AND_COLOR_LIST)
from weather_lk.core.Data import Data

log = Log('SummaryDataCharts')


class SummaryDataCharts:
    N_ANNOTATE = 10

    @staticmethod
    def draw_temp_chart_for_place(place, data_for_place):
        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data_for_place]
        y_max_temp = [d['max_temp'] for d in data_for_place]
        y_min_temp = [d['min_temp'] for d in data_for_place]

        y_max_temp_not_null = [y for y in y_max_temp if y is not None]
        if len(y_max_temp_not_null) < 10:
            return

        plt.close()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        plt.title(f'{place}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')

        x, y_min_temp, y_max_temp = zip(
            *[
                z
                for z in zip(x, y_min_temp, y_max_temp)
                if (z[1] is not None) and (z[2] is not None)
            ]
        )

        min_temp = min(y_min_temp) - 1
        max_temp = max(y_max_temp) + 1
        plt.ylim([min_temp, max_temp])
        width = 1

        sorted_max_pairs = sorted(
            list(zip(x, y_max_temp)),
            key=lambda x: x[1],
            reverse=True,
        )
        for i, [xi, yi] in enumerate(
            sorted_max_pairs[: SummaryDataCharts.N_ANNOTATE]
        ):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}°C {date_str}'
            xy = (xi, yi)
            xytext = (xi, max_temp - i)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='r')

        sorted_min_pairs = sorted(
            list(zip(x, y_min_temp)),
            key=lambda x: x[1],
        )
        for i, [xi, yi] in enumerate(
            sorted_min_pairs[: SummaryDataCharts.N_ANNOTATE]
        ):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}°C {date_str}'
            xy = (xi, yi)
            xytext = (xi, min_temp + i)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='b')

        for [limit, color] in LIMIT_AND_COLOR_LIST:
            q = list(
                zip(
                    *[
                        z
                        for z in zip(x, y_max_temp)
                        if (limit <= z[1] < limit + 5)
                    ]
                )
            )
            if not q:
                continue
            x2, y_max_temp2 = q
            plt.bar(
                x2,
                y_max_temp2,
                color=color,
                width=width,
            )

        plt.bar(x, y_min_temp, color='w', width=width)

        y_temp_mid = [(a + b) / 2 for a, b in zip(y_min_temp, y_max_temp)]
        window = 7
        y_temp_mid_rolling = [
            sum(y_temp_mid[i: i + window]) / window
            for i in range(len(y_temp_mid) - window + 1)
        ]
        x_rolling = x[: -(window - 1)]
        plt.plot(x_rolling, y_temp_mid_rolling, color='black')

        label = SummaryWriteDataByPlace.get_place_label(place)
        image_path = os.path.join(DIR_DATA_CHARTS_TEMPERATURE, f'{label}.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')
        # os.startfile(image_path)

    @staticmethod
    def draw_rain_chart_for_place(place, data_for_place):
        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data_for_place]
        y_rain = [d['rain'] for d in data_for_place]

        y_rain_not_null = [y for y in y_rain if y is not None]
        if len(y_rain_not_null) < 10:
            return

        plt.close()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        plt.title(f'{place}')
        plt.xlabel('Date')
        plt.ylabel('Rainfall (mm)')

        x, y_rain = zip(*[z for z in zip(x, y_rain) if (z[1] is not None)])

        width = 1

        sorted_max_pairs = sorted(
            list(zip(x, y_rain)),
            key=lambda x: x[1],
            reverse=True,
        )

        rain_max = max(max(y_rain), 200)
        plt.ylim([0, rain_max])

        for i, [xi, yi] in enumerate(
            sorted_max_pairs[: SummaryDataCharts.N_ANNOTATE]
        ):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.0f}mm {date_str}'
            xy = (xi, yi)
            xytext = (xi, rain_max - i * 4)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='b')

        plt.bar(x, y_rain, color='b', width=width)

        label = SummaryWriteDataByPlace.get_place_label(place)
        image_path = os.path.join(DIR_DATA_CHARTS_RAINFALL, f'{label}.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')
        # os.startfile(image_path)

    def draw_charts_by_place(self):
        if not os.path.exists(DIR_DATA_CHARTS):
            os.makedirs(DIR_DATA_CHARTS)
        if not os.path.exists(DIR_DATA_CHARTS_RAINFALL):
            os.makedirs(DIR_DATA_CHARTS_RAINFALL)
        if not os.path.exists(DIR_DATA_CHARTS_TEMPERATURE):
            os.makedirs(DIR_DATA_CHARTS_TEMPERATURE)

        idx_by_place = Data.idx_by_place()
        for place in DISPLAY_PLACES:
            data_for_place = idx_by_place.get(place, None)
            if data_for_place is None:
                log.warning(f'No data for {place}')
                continue

            try:
                SummaryDataCharts.draw_temp_chart_for_place(
                    place, data_for_place
                )
            except Exception as e:
                log.error(f'draw_charts_by_place - {place}: {str(e)}')

            try:
                SummaryDataCharts.draw_rain_chart_for_place(
                    place, data_for_place
                )
            except Exception as e:
                log.error(f'draw_rain_chart_for_place - {place}: {str(e)}')
