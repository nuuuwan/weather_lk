"""Daily Weather Report."""

import re

import tabula
from utils import jsonx, timex

from weather_lk._constants import (REGEX_DATE, REGEX_HIGHEST, REGEX_NON_ASCII,
                                   REGEX_PLACE_RAIN_2, REGEX_PLACE_TEMP_RAIN)
from weather_lk._utils import _get_location, _parse_float, log


def _get_lines(pdf_file):
    df = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)[0]
    row_k_to_items = {}
    for _, cell_map in df.to_dict().items():
        for row_k, cell_vallue in cell_map.items():
            if row_k not in row_k_to_items:
                row_k_to_items[row_k] = []
            row_k_to_items[row_k].append(cell_vallue)

    lines = []
    for row_k, items in row_k_to_items.items():
        lines.append(
            ' '.join(
                list(
                    map(
                        lambda item: re.sub(
                            REGEX_NON_ASCII, '', str(item)
                        ).strip(),
                        items,
                    )
                )
            )
        )
    return lines


def _parse_and_dump(date_id, pdf_file):
    lines = _get_lines(pdf_file)

    place_to_weather = {}
    date_ut = None
    for line in lines:
        line = re.sub(r'\s+', ' ', line).strip()
        line = line.replace('polonnaruwa', 'Polonnaruwa')
        line = line.replace('Omqrh', '')

        result = re.search(REGEX_DATE, line)
        if result:
            date_str = result.groupdict()['date_str']
            date_ut = timex.parse_time(date_str, '%Y.%m.%d')
            continue

        result = re.search(REGEX_PLACE_TEMP_RAIN, line)
        if result:
            data = result.groupdict()
            place = data['place'].strip()

            place_to_weather[place] = {
                'place': place,
                'temp_min': _parse_float(data['min_temp_str']),
                'temp_max': _parse_float(data['max_temp_str']),
                'rain': _parse_float(data['rain_str']),
                'lat_lng': _get_location(place),
            }
            continue

        result = re.search(REGEX_PLACE_RAIN_2, line)
        if result:
            data = result.groupdict()
            for i in [1, 2]:
                place = data['place%d' % i].strip()
                rain = _parse_float(data['rain%d_str' % i])
                place_to_weather[place] = {
                    'place': place,
                    'rain': rain,
                    'lat_lng': _get_location(place),
                }
            continue

        result = re.search(REGEX_HIGHEST, line)
        if result:
            data = result.groupdict()
            place_to_weather[place] = {
                'place': place,
                'rain': _parse_float(data['rain_str']),
                'lat_lng': _get_location(place),
            }
            continue

    min_temp, min_temp_place = None, None
    max_temp, max_temp_place = None, None
    max_rain, max_rain_place = None, None
    for place, weather in place_to_weather.items():
        place_min_temp = weather.get('temp_min', 1000)
        place_max_temp = weather.get('temp_max', -1000)
        place_rain = weather.get('rain', 0)
        if place_min_temp and (not min_temp or place_min_temp < min_temp):
            min_temp, min_temp_place = place_min_temp, place
        if place_max_temp and (not max_temp or place_max_temp > max_temp):
            max_temp, max_temp_place = place_max_temp, place
        if place_rain and (not max_rain or place_rain > max_rain):
            max_rain, max_rain_place = place_rain, place

    data = {
        'date_ut': date_ut,
        'date': timex.format_time(date_ut, '%Y-%m-%d'),
        'min_temp': {
            'place': min_temp_place,
            'temp': min_temp,
        },
        'max_temp': {
            'place': max_temp_place,
            'temp': max_temp,
        },
        'max_rain': {
            'place': max_rain_place,
            'rain': max_rain,
        },
        'weather_list': list(place_to_weather.values()),
    }

    data_file = '/tmp/weather_lk.%s.json' % (date_id)
    jsonx.write(data_file, data)
    log.info(
        '%s: Wrote data to %s',
        date_id,
        data_file,
    )
    return data
