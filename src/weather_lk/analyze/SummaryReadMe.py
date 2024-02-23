import os

from utils import File, Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import DIR_REPO, DISPLAY_PLACES, URL_REMOTE_DATA

log = Log('SummaryReadMe')


class SummaryReadMe:
    def build_readme(self):
        temp_lines = []
        rain_lines = []
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
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
                + '[Department of Meteorology](http://www.meteo.gov.lk/), '
                + 'Sri Lanka',
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
