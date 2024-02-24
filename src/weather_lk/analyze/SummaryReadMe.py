import os

from utils import File, Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import (COVERAGE_WINDOW_LIST, DIR_REPO,
                                  DISPLAY_PLACES, TEMPERATURE_CHART_WINDOWS,
                                  URL_REMOTE_DATA)

log = Log('SummaryReadMe')

DELIM_COLUMN = ' | '


def build_row(values):
    return DELIM_COLUMN + DELIM_COLUMN.join(values) + DELIM_COLUMN


def build_table(keys, values_list):
    sep = [(' ---- ' if 'id' in key else ' ---: ') for key in keys]
    lines = [
        build_row(keys),
        build_row(sep),
    ]
    for values in values_list:
        lines.append(build_row(values))
    return lines


class SummaryReadMe:
    @property
    def lines_country(self):
        lines = []
        lines.extend(
            [
                '## Weather Nationwide :sri_lanka:',
                '',
                f'![Temperature]({URL_REMOTE_DATA}'
                + '/charts/country_temperature.png)',
                '',
                f'![Rainfall]({URL_REMOTE_DATA}/charts/country_rainfall.png)',
                '',
            ]
        )
        return lines

    def get_lines_temperature(self, window):
        title = 'Temperature 🌡️'
        if window:
            title += f' (Last {window} days)'
        lines = [f'# {title}', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
            if window:
                label += f'-{window}days'
            image_path_temp = (
                URL_REMOTE_DATA + '/charts/temperature/' + f'{label}.png'
            )
            lines.extend(
                [
                    f'## {place} 🌡️',
                    '',
                    f'![{place}]({image_path_temp})',
                    '',
                ]
            )
        return lines

    @property
    def lines_rainfall(self):
        lines = ['# Rainfall', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
            image_path_rain = (
                URL_REMOTE_DATA + '/charts/rainfall/' + f'{label}.png'
            )
            lines.extend(
                [
                    f'## {place} 🌧️',
                    '',
                    f'![{place}]({image_path_rain})',
                    '',
                ]
            )
        return lines

    @property
    def lines_coverage(self):
        lines = [
            '# Coverage',
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
    def lines_source_stats(self):
        source_to_stats = self.source_to_stats
        keys = [
            'n',
            'n_parse_attempted',
            'n_parse_successful',
            'n_parse_failed',
            'min_date',
            'max_date',
        ]
        values_list = []
        for source_id, stats in source_to_stats.items():
            values = [f'`{source_id}`'] + [
                str(stats.get(key, '')) for key in keys
            ]
            values_list.append(values)
        return ['# Source Statistics', ''] + build_table(
            [
                'source_id',
            ]
            + keys,
            values_list,
        )

    @property
    def lines_source_stats_year_to_n(self):
        source_to_stats = self.source_to_stats
        keys = [str(year) for year in range(2024, 2024 - 11, -1)]
        values_list = []
        for source_id, stats in source_to_stats.items():
            values = [f'`{source_id}`'] + [
                str(stats['year_to_n'].get(year, 0)) for year in keys
            ]
            values_list.append(values)
        return ['', '## By Year', ''] + build_table(
            [
                'source_id',
            ]
            + keys,
            values_list,
        )

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

    def build_sub_readmes(self):
        links = []

        for window in TEMPERATURE_CHART_WINDOWS:
            temperature_infos = [
                (
                    f'temperature_by_city_(_last_{window}_days)',
                    self.get_lines_temperature(window),
                ),
            ]

        for id, lines in temperature_infos + [
            ('rainfall_by_city', self.lines_rainfall),
            ('data_coverage', self.lines_coverage),
            (
                'source_statistics',
                self.lines_source_stats + self.lines_source_stats_year_to_n,
            ),
        ]:
            readme_path = os.path.join(DIR_REPO, f'README.{id}.md')
            lines = [line.strip() for line in lines]
            File(readme_path).write_lines(lines)
            log.info(f'Wrote {readme_path}')
            title = id.replace('_', ' ').title()
            links.append(f'* [{title}](README.{id}.md)')
        return links

    def build_readme(self):
        # sub readmes
        links = self.build_sub_readmes()

        lines = (
            self.lines_header
            + self.lines_country
            + [
                '## More Information',
                '',
            ]
            + links
        )
        readme_path = os.path.join(DIR_REPO, 'README.md')
        File(readme_path).write_lines(lines)
        log.info(f'Wrote README to {readme_path}')
