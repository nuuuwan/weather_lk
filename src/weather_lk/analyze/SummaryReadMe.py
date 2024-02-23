import os

from utils import File, Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import (COVERAGE_WINDOW_LIST, DIR_REPO,
                                  DISPLAY_PLACES, URL_REMOTE_DATA)

log = Log('SummaryReadMe')


class SummaryReadMe:
    @property
    def lines_country(self):
        lines = []
        lines.extend(
            [
                '## Weather Nationwide :sri_lanka:', 
                '',
                f'![Temperature]({URL_REMOTE_DATA}/charts/country_temperature.png)',
                '',
                f'![Rainfall]({URL_REMOTE_DATA}/charts/country_rainfall.png)',
                '',
            ]
        )
        return lines
    @property
    def lines_temperature(self):
        lines = ['## Temperature', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
            image_path_temp = (
                URL_REMOTE_DATA + '/charts/temperature/' + f'{label}.png'
            )
            lines.extend(
                [
                    f'### {place} 🌡️',
                    '',
                    f'![{place}]({image_path_temp})',
                    '',
                ]
            )
        return lines

    @property
    def lines_rainfall(self):
        lines = ['## Rainfall', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
            image_path_rain = (
                URL_REMOTE_DATA + '/charts/rainfall/' + f'{label}.png'
            )
            lines.extend(
                [
                    f'### {place} 🌧️',
                    '',
                    f'![{place}]({image_path_rain})',
                    '',
                ]
            )
        return lines

    @property
    def lines_coverage(self):
        lines = [
            '## Coverage',
            '',
        ]

        for window in COVERAGE_WINDOW_LIST:
            lines.extend(
                [
                    f'### Last {window:,} days',
                    '',
                    f'![Coverage]({URL_REMOTE_DATA}/coverage-{window}days.png)',
                    '',
                ]
            )

        return lines

    @property
    def lines_header(self):
        return [
            '# Sri Lanka :sri_lanka: Weather (weather_lk)',
            '',
            'Rainfall and Temperature data, extracted from the '
            + '[Department of Meteorology](http://www.meteo.gov.lk/), '
            + 'Sri Lanka',
            '',
        ]

    def build_readme(self):
        lines = (
            self.lines_header
            + self.lines_country
            + self.lines_temperature
            + self.lines_rainfall
            + self.lines_coverage
        )
        readme_path = os.path.join(DIR_REPO, 'README.md')
        File(readme_path).write_lines(lines)
        log.info(f'Wrote README to {readme_path}')
