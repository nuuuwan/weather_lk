"""Daily Weather Report."""

import os
import re

import camelot
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import WWW, JSONFile, Time, TimeFormat

from weather_lk._constants import REGEX_DATE, REGEX_NON_ASCII, URL
from weather_lk._utils import log

PAGE_LOAD_TIMEOUT = 120
FORMAT_DATE_ID = '%Y-%m-%d'


def clean_location_name(cell):
    cell = re.sub(REGEX_NON_ASCII, '', cell)
    cell = re.sub(r'\s+', ' ', cell)
    cell = cell.strip()
    cell = cell.replace('wkqrdOmqrh', '')
    cell = cell.replace('polonnaruwa', 'Polonnaruwa')
    cell = ' '.join(
        list(
            filter(
                lambda word: len(word) > 0 and (word[0] != word[0].lower()),
                cell.split(' '),
            )
        )
    )
    return cell


def clean_cell(cell):
    cell = re.sub(REGEX_NON_ASCII, '', cell)
    cell = re.sub(r'\s+', ' ', cell)
    cell = cell.strip()
    return cell


def clean_row(row):
    return list(
        map(
            clean_cell,
            row,
        )
    )


def parse_float(x):
    try:
        return (float)(x)
    except ValueError:
        return None


def get_file(date_id, ext):
    return f'/tmp/weather_lk.{date_id}.{ext}'


def scrape(date_id):
    """Get daily weather report."""
    pdf_file = get_file(date_id, 'pdf')
    if os.path.exists(pdf_file):
        log.warning(f'{pdf_file} exists. Not downloading')
        return

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    browser.get(URL)
    a_daily = browser.find_element("xpath", "//a[text()='Daily Rainfall']")
    pdf_url = a_daily.get_attribute('href')
    browser.quit()

    WWW(pdf_url).downloadBinary(pdf_file)
    log.info(f'Downloaded {pdf_url} to {pdf_file}')


def parse(date_id):
    pdf_file = get_file(date_id, 'pdf')
    tables = camelot.read_pdf(pdf_file, pages='all')

    csv_file = get_file(date_id, 'csv')
    tables.export(csv_file, f='csv')
    log.info(f'Wrote {csv_file}')

    table = tables[0].df.values.tolist()

    ut = None
    weather_list = []

    for row in table:
        row = clean_row(row)
        row_str = ' '.join(row)
        result = re.search(REGEX_DATE, row_str)
        if result:
            date_str = result.groupdict().get('date_str')
            ut = TimeFormat('%Y.%m.%d').parse(date_str).ut
            continue

        if row[0] != '' and row[-1] == '':
            place_str, max_temp_str, min_temp_str, rain_str, _ = row

            place = clean_location_name(place_str)
            min_temp = parse_float(min_temp_str)
            max_temp = parse_float(max_temp_str)
            rain = parse_float(rain_str)

            if rain is not None:
                weather_list.append(
                    dict(
                        place=place,
                        min_temp=min_temp,
                        max_temp=max_temp,
                        rain=rain,
                    )
                )
                continue

        if row[0] != '' and row[-2] == '':
            place_str1, rain_str1, place_str2, _, rain_str2 = row

            place1 = clean_location_name(place_str1)
            place2 = clean_location_name(place_str2)
            rain1 = parse_float(rain_str1)
            rain2 = parse_float(rain_str2)

            if rain1 is not None:
                weather_list.append(
                    dict(
                        place=place1,
                        rain=rain1,
                    )
                )
                continue

            if rain2 is not None:
                weather_list.append(
                    dict(
                        place=place2,
                        rain=rain2,
                    )
                )
                continue

    min_temp = None
    min_temp_place = None
    max_temp = None
    max_temp_place = None
    max_rain = None
    max_rain_place = None

    for weather in weather_list:
        place = weather.get('place')
        _min_temp = weather.get('min_temp')
        _max_temp = weather.get('max_temp')
        rain = weather.get('rain')

        if _min_temp:
            if min_temp is None or min_temp > _min_temp:
                min_temp = _min_temp
                min_temp_place = place

        if _max_temp:
            if max_temp is None or max_temp < _max_temp:
                max_temp = _max_temp
                max_temp_place = place

        if rain:
            if max_rain is None or max_rain < rain:
                max_rain = rain
                max_rain_place = place

    data = {
        'date_ut': ut,
        'date': TimeFormat('%Y-%m-%d').stringify(Time.now()),
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
        'weather_list': weather_list,
    }

    doc_date_id = TimeFormat('%Y-%m-%d').stringify(Time(ut))
    if doc_date_id != date_id:
        log.error(f'Invalid doc_date_id: {doc_date_id} != {date_id}')
        os.system(f'rm {pdf_file}')
        os.system(f'rm {csv_file}')
        return

    json_file = get_file(date_id, 'json')
    JSONFile(json_file).write(data)
    log.info(f'Wrote {json_file}')
    return data


def load(date_id):
    """Load daily weather report."""

    json_file = get_file(date_id, 'json')
    if os.path.exists(json_file):
        data = JSONFile(json_file).read()
        n_places = len(data['weather_list'])
        log.info(f'Loaded data for {n_places} locally, from {json_file}')
        return data

    url = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan/weather_lk/data',
        'weather_lk.%s.json' % date_id,
    )
    if WWW(url).exists:
        data = WWW(url).readJSON()
        n_places = len(data['weather_list'])
        log.info(f'Loaded data for {n_places} remotely, from {url}')
        return data

    log.error('No data for %s', date_id)
    return None


if __name__ == '__main__':
    date_id = TimeFormat(FORMAT_DATE_ID).stringify(Time.now())
    scrape(date_id)
    parse(date_id)
