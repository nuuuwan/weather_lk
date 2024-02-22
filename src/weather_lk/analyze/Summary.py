import os
from datetime import datetime
from functools import cache, cached_property

import matplotlib.pyplot as plt
from utils import JSONFile, Log, TSVFile

from weather_lk.constants import (DIR_DATA_BY_PLACE, DIR_DATA_CHARTS, DIR_REPO,
                                  DIR_REPO_DAILY_DATA, LIMIT_AND_COLOR_LIST)
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

log = Log('Summary')


class Summary:
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
    N_ANNOTATE = 10

    @cached_property
    def data_by_place(self):
        idx = {}
        for data in self.data_list:
            date = data['date']
            for item in data['weather_list']:
                place = item['place']
                d = dict(
                    date=date,
                    rain=item['rain'],
                    temp_min=item.get('min_temp', item.get('temp_min', None)),
                    temp_max=item.get('max_temp', item.get('temp_max', None)),
                )

                if place not in idx:
                    idx[place] = []
                idx[place].append(d)

        new_idx = {}
        for place, data_for_place in sorted(idx.items(), key=lambda x: x[0]):
            sorted_data_for_place = sorted(
                data_for_place, key=lambda x: x['date'], reverse=True
            )
            new_idx[place] = sorted_data_for_place
        return new_idx

    @cached_property
    def data_list(self):
        data_list = []
        for file_only in os.listdir(DIR_REPO_DAILY_DATA):
            if not (
                file_only.startswith('weather_lk.')
                and file_only.endswith('.json')
            ):
                continue
            file_path = os.path.join(DIR_REPO_DAILY_DATA, file_only)
            data = JSONFile(file_path).read()
            data_list.append(data)
        data_list = sorted(data_list, key=lambda x: x['date'])
        min_date = data_list[0]['date']
        max_date = data_list[-1]['date']

        n = len(data_list)
        log.info(
            f'Loaded data for {n:,} days, '
            + f'from {min_date} to {max_date}.'
        )
        return data_list

    @staticmethod
    def __write_json(label, x):
        summary_json_path = os.path.join(DIR_REPO, f'{label}.json')
        JSONFile(summary_json_path).write(x)
        file_size_m = os.path.getsize(summary_json_path) / 1024 / 1024
        log.info(
            f'Wrote summary to {summary_json_path} ({file_size_m:.2f} MB)'
        )

    def write(self):
        Summary.__write_json('data_list', self.data_list)
        Summary.__write_json('data_by_place', self.data_by_place)

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

        for place, data_for_place in self.data_by_place.items():
            try:
                Summary.__write_for_place(place, data_for_place)
            except Exception as e:
                log.error(f'Error writing data for {place}: {str(e)}')

    @staticmethod
    def draw_temp_chart_for_place(place, data_for_place):
        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data_for_place]
        y_temp_max = [d['temp_max'] for d in data_for_place]
        y_temp_min = [d['temp_min'] for d in data_for_place]

        plt.close()
        fig = plt.gcf()
        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        plt.title(f'{place}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')

        x, y_temp_min, y_temp_max = zip(
            *[
                z
                for z in zip(x, y_temp_min, y_temp_max)
                if (z[1] is not None) and (z[2] is not None)
            ]
        )

        temp_min = min(y_temp_min) - 1
        temp_max = max(y_temp_max) + 1
        plt.ylim([temp_min, temp_max])
        width = 1

        sorted_max_pairs = sorted(
            list(zip(x, y_temp_max)),
            key=lambda x: x[1],
            reverse=True,
        )
        for i, [xi, yi] in enumerate(sorted_max_pairs[: Summary.N_ANNOTATE]):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}°C {date_str}'
            xy = (xi, yi)
            xytext = (xi, temp_max - i)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='r')

        sorted_min_pairs = sorted(
            list(zip(x, y_temp_min)),
            key=lambda x: x[1],
        )
        for i, [xi, yi] in enumerate(sorted_min_pairs[: Summary.N_ANNOTATE]):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}°C {date_str}'
            xy = (xi, yi)
            xytext = (xi, temp_min + i)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color='b')

        for [limit, color] in LIMIT_AND_COLOR_LIST:
            q = list(
                zip(
                    *[
                        z
                        for z in zip(x, y_temp_max)
                        if (limit <= z[1] < limit + 5)
                    ]
                )
            )
            if not q:
                continue
            x2, y_temp_max2 = q
            plt.bar(
                x2,
                y_temp_max2,
                color=color,
                width=width,
            )

        plt.bar(x, y_temp_min, color='w', width=width)

        y_temp_mid = [(a + b) / 2 for a, b in zip(y_temp_min, y_temp_max)]
        window = 7
        y_temp_mid_rolling = [
            sum(y_temp_mid[i: i + window]) / window
            for i in range(len(y_temp_mid) - window + 1)
        ]
        x_rolling = x[: -(window - 1)]
        plt.plot(x_rolling, y_temp_mid_rolling, color='black')

        label = Summary.get_place_label(place)
        image_path = os.path.join(DIR_DATA_CHARTS, f'{label}.temperature.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')
        # os.startfile(image_path)

    @staticmethod
    def draw_rain_chart_for_place(place, data_for_place):
        x = [datetime.strptime(d['date'], '%Y-%m-%d') for d in data_for_place]
        y_rain = [d['rain'] for d in data_for_place]

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
        image_path = os.path.join(DIR_DATA_CHARTS, f'{label}.rainfall.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')
        # os.startfile(image_path)

    def draw_charts_by_place(self):
        if not os.path.exists(DIR_DATA_CHARTS):
            os.makedirs(DIR_DATA_CHARTS)
        for place, data_for_place in self.data_by_place.items():
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


# def test(places):
#     if not os.path.exists(DIR_DATA_CHARTS):
#         os.makedirs(DIR_DATA_CHARTS)
#     s = Summary()
#     idx = s.data_by_place

#     for place in places:
#         if place not in idx:
#             log.error(f'No data for {place}')
#             continue
#         data = idx[place]
#         Summary.draw_temp_chart_for_place(place, data)
#         Summary.draw_rain_chart_for_place(place, data)


# if __name__ == "__main__":
#     test(['Colombo'])
