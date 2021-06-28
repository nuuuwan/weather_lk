"""Daily Weather Report."""

import re

import tabula

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from PyPDF2 import PdfFileReader

from utils import www, timex, jsonx, dt

from weather_lk._utils import log

URL = 'https://www.meteo.gov.lk/index.php?lang=en'
REGEX_DATE = r'.+(?P<date_y>\d{4})-(?P<date_m>\d{2})-(?P<date_d>\d{2}).+'

REGEX_TEMP = r'(?P<temp>\d{2}\.\d{1})'


def _parse_float(float_str):
    if float_str == 'NA':
        return None
    return dt.parse_float(float_str)


def _parse_pdf(date_id, pdf_file):
    df = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)[0]
    d = df.to_dict()
    row_k_to_line_items = {}
    for col_k, cell_map in d.items():
        for row_k, cell_vallue in cell_map.items():
            if row_k not in row_k_to_line_items:
                row_k_to_line_items[row_k] =[]
            row_k_to_line_items[row_k].append(cell_vallue)

    lines = []
    for row_k, line_items in row_k_to_line_items.items():
        lines.append(' '.join(list(map(
            lambda line_item: \
                re.sub(r'[^\x00-\x7F]+', '', str(line_item)).strip(),
            line_items,
        ))))

    REGEX_DATE = r'(?P<date_str>\d{4}\.\d{2}\.\d{2})'
    REGEX_PLACE_TEMP_RAIN = r'(?P<place>([A-Z][a-z]+\s*)+) (?P<max_temp_str>((\d+\.\d+)+|NA)) (?P<min_temp_str>((\d+\.\d+)+|NA)) (?P<rain_str>((\d+\.\d+)+|NA))'
    REGEX_PLACE_RAIN_2 = r'(?P<place1>([A-Z][a-z]+\s*)+) (?P<rain1_str>((\d+\.\d+)+|NA)) (?P<place2>([A-Z][a-z]+\s*)+) (?P<rain2_str>((\d+\.\d+)+|NA))'
    REGEX_HIGHEST = r'(?P<rain_str>((\d+\.\d+)+|NA)) mm (?P<place>([A-Z][a-z]+\s*)+)'

    place_to_weather = {}
    date_ut = None
    for line in lines:
        line = re.sub('\s+', ' ', line).strip()
        line = line.replace('polonnaruwa', 'Polonnaruwa')
        result = re.search(REGEX_DATE, line)
        if result:
            date_str = result.groupdict()['date_str']
            date_ut = timex.parse_time(date_str, '%Y.%m.%d')
            continue

        result = re.search(REGEX_PLACE_TEMP_RAIN, line)
        if result:
            data = result.groupdict()
            place = data['place']
            temp_max = _parse_float(data['max_temp_str'])
            temp_min = _parse_float(data['min_temp_str'])
            rain = _parse_float(data['rain_str'])

            place_to_weather[place] = {
                'place': place,
                'temp_min': temp_min,
                'temp_max': temp_max,
                'rain': rain,
            }
            continue

        result = re.search(REGEX_PLACE_RAIN_2, line)
        if result:
            data = result.groupdict()
            place1 = data['place1']
            rain1 = _parse_float(data['rain1_str'])
            place2 = data['place2']
            rain2 = _parse_float(data['rain2_str'])

            place_to_weather[place1] = {'place': place1, 'rain': rain1}
            place_to_weather[place2] = {'place': place2, 'rain': rain2}
            continue

        result = re.search(REGEX_HIGHEST, line)
        if result:
            data = result.groupdict()
            place = data['place']
            rain = _parse_float(data['rain_str'])

            place_to_weather[place] = {'place': place, 'rain': rain}
            continue

        log.warn('Not parsed: %s', line)

    min_temp, min_temp_place = None, None
    max_temp, max_temp_place = None, None
    max_rain, max_rain_place = None, None
    for place, weather in place_to_weather.items():
        place_min_temp = weather.get('temp_min', 1000)
        place_max_temp = weather.get('temp_max', -1000)
        place_rain = weather.get('rain', 0)

        if place_min_temp and (not min_temp or place_min_temp < min_temp):
            min_temp = place_min_temp
            min_temp_place = place

        if place_max_temp and (not max_temp or place_max_temp > max_temp):
            max_temp = place_max_temp
            max_temp_place = place

        if place_rain and (not max_rain or place_rain > max_rain):
            max_rain = place_rain
            max_rain_place = place

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


def _load_pdf_file():
    """Get daily weather report."""
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    a_daily = browser.find_element_by_xpath(
        "//a[text()='Daily Rainfall']"
    )
    pdf_url = a_daily.get_attribute('href')
    browser.quit()

    result = re.search(REGEX_DATE, pdf_url)
    if result:
        result_data = result.groupdict()
        unixtime = timex.parse_time(
            '%s-%s-%s' % (
                result_data['date_y'],
                result_data['date_m'],
                result_data['date_d'],
            ),
            '%Y-%m-%d',
        )
    else:
        unixtime = timex.get_unixtime()

    date_id = timex.format_time(unixtime, '%Y%m%d')
    pdf_file = '/tmp/weather_lk.%s.pdf' % (date_id)
    www.download_binary(pdf_url, pdf_file)
    log.info('%s: Downloaded %s to %s', date_id, pdf_url, pdf_file)

    return date_id, pdf_file


def _back_populate(date_ut):
    pass


def daily_weather_report():
    """Get daily weather report."""
    # date_id, pdf_file = _load_pdf_file()
    # data = _parse_pdf(date_id, pdf_file)
    # _back_populate(data['date_ut'])
    _back_populate(1624732200)


if __name__ == '__main__':
    daily_weather_report()
