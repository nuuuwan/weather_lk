import os
from datetime import datetime
from functools import cache

import matplotlib.pyplot as plt
from utils import (
    SECONDS_IN,
    TIME_FORMAT_DATE,
    File,
    JSONFile,
    Log,
    Time,
    TSVFile,
)

from weather_lk.constants import (
    DIR_DATA_BY_PLACE,
    DIR_DATA_CHARTS,
    DIR_DATA_CHARTS_RAINFALL,
    DIR_DATA_CHARTS_TEMPERATURE,
    DIR_REPO,
    LIMIT_AND_COLOR_LIST,
    URL_REMOTE_DATA,
)
from weather_lk.core.Data import Data
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

log = Log('Summary')


class Summary:
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
    N_ANNOTATE = 10

    @staticmethod
    def __write_json(label, x):
        summary_json_path = os.path.join(DIR_REPO, f'{label}.json')
        JSONFile(summary_json_path).write(x)
        file_size_m = os.path.getsize(summary_json_path) / 1024 / 1024
        log.info(
            f'Wrote summary to {summary_json_path} ({file_size_m:.2f} MB)'
        )

    def write(self):
        Summary.__write_json('list_all', Data.list_all())
        Summary.__write_json('idx_by_place', Data.idx_by_place())
        Summary.__write_json('idx_by_date', Data.idx_by_date())

    @staticmethod
    @cache
    def get_place_label(place):
        lat, lng = Summary.PLACE_TO_LATLNG[place]
        place_id = place.replace(' ', '-')
        return f'{lng:.2f}E-{lat:.2f}N-{place_id}'

    @staticmethod
    def __write_for_place(place, data_for_place):
        label = Summary.get_place_label(place)
        n = len(data_for_place)

        json_path = os.path.join(DIR_DATA_BY_PLACE, f'{label}.json')
        JSONFile(json_path).write(data_for_place)

        tsv_path = os.path.join(DIR_DATA_BY_PLACE, f'{label}.tsv')
        TSVFile(tsv_path).write(data_for_place)

        log.info(f'Wrote {json_path}/tsv ({n} records)')

    def write_by_place(self):
        if not os.path.exists(DIR_DATA_BY_PLACE):
            os.makedirs(DIR_DATA_BY_PLACE)

        for place, data_for_place in Data.idx_by_place().items():
            try:
                Summary.__write_for_place(place, data_for_place)
            except Exception as e:
                log.error(f'Error writing data for {place}: {str(e)}')

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
        for i, [xi, yi] in enumerate(sorted_max_pairs[: Summary.N_ANNOTATE]):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}°C {date_str}'
            xy = (xi, yi)
            xytext = (xi, max_temp - i)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='r')

        sorted_min_pairs = sorted(
            list(zip(x, y_min_temp)),
            key=lambda x: x[1],
        )
        for i, [xi, yi] in enumerate(sorted_min_pairs[: Summary.N_ANNOTATE]):
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

        label = Summary.get_place_label(place)
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

        for i, [xi, yi] in enumerate(sorted_max_pairs[: Summary.N_ANNOTATE]):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.0f}mm {date_str}'
            xy = (xi, yi)
            xytext = (xi, rain_max - i * 4)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='b')

        plt.bar(x, y_rain, color='b', width=width)

        label = Summary.get_place_label(place)
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

        for place, data_for_place in Data.idx_by_place().items():
            try:
                Summary.draw_temp_chart_for_place(place, data_for_place)
            except Exception as e:
                log.error(
                    f'Error drawing temperature chart for {place}: {str(e)}'
                )

            try:
                Summary.draw_rain_chart_for_place(place, data_for_place)
            except Exception as e:
                log.error(
                    f'Error drawing rainfall chart for {place}: {str(e)}'
                )

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

    def build_readme(self):
        display_places = [
            # LK-11 Colombo
            'Colombo',
            'Rathmalana',
            # LK-12 Gampaha
            'Katunayake',
            # LK-13 Kalutara
            # LK-21 Kandy
            'Katugasthota',
            # LK-22 Matale
            # LK-23 Nuwara Eliya
            'Nuwara Eliya',
            # LK-31 Galle
            'Galle',
            # LK-32 Matara
            # LK-33 Hambantota
            'Hambanthota',
            # LK-41 Jaffna
            'Jaffna',
            # LK-42 Mannar
            'Mannar',
            # LK-43 Vavuniya
            'Vavuniya',
            # LK-44 Mullaitivu
            'Mullaithivu',
            # LK-45 Kilinochchi
            # LK-51 Batticaloa
            'Batticaloa',
            # LK-52 Ampara
            'Pothuvil',
            # LK-53 Trincomalee
            'Trincomalee',
            # LK-61 Kurunegala
            'Kurunagala',
            # LK-62 Puttalam
            'Puttalam',
            # LK-71 Anuradhapura
            'Anuradhapura',
            'Maha Illuppallama',
            # LK-72 Polonnaruwa
            'Polonnaruwa',
            # LK-81 Badulla
            'Badulla',
            'Bandarawela',
            # LK-82 Moneragala
            'Monaragala',
            # LK-91 Ratnapura
            'Rathnapura',
            # LK-92 Kegalle
        ]

        temp_lines = []
        rain_lines = []
        for place in display_places:
            label = Summary.get_place_label(place)
            image_path_temp = (
                URL_REMOTE_DATA + '/charts/temperature/' + f'{label}.png'
            )
            image_path_rain = (
                URL_REMOTE_DATA + '/charts/rainfall/' + f'{label}.png'
            )
            temp_lines.extend(
                [
                    f'### {place}',
                    '',
                    f'![{place}]({image_path_temp})',
                    '',
                ]
            )

            rain_lines.extend(
                [
                    f'### {place}',
                    '',
                    f'![{place}]({image_path_rain})',
                    '',
                ]
            )

        lines = (
            [
                '# Sri Lanka :sri_lanka: Weather (weather_lk)',
                '',
                'Rainfall and Temperature data, extracted from the '
                + '[Sri Lanka Meteorological Department](http://www.meteo.gov.lk/).',
                '',
                '## Coverage',
                '',
                '### Last 10 days',
                '',
                f'![Coverage]({URL_REMOTE_DATA}/coverage-10days.png)',
                '',
                '### Last 100 days',
                '',
                f'![Coverage]({URL_REMOTE_DATA}/coverage-100days.png)',
                '',
                '### Last 1,000 days',
                '',
                f'![Coverage]({URL_REMOTE_DATA}/coverage-1000days.png)',
                '',
                '## Charts - Temperature',
                '',
            ]
            + temp_lines
            + ['## Charts - Rainfall', '']
            + rain_lines
            + [
                '',
            ]
        )
        readme_path = os.path.join(DIR_REPO, 'README.md')
        File(readme_path).write_lines(lines)
        log.info(f'Wrote README to {readme_path}')

    def write_all(self):
        self.write()
        self.write_by_place()
        self.draw_charts_by_place()
        self.write_coverage()
        self.build_readme()
