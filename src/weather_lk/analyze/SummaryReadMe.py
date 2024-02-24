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
                f'![Temperature]({URL_REMOTE_DATA}'
                + '/charts/country_temperature.png)',
                '',
                f'![Rainfall]({URL_REMOTE_DATA}/charts/country_rainfall.png)',
                '',
            ]
        )
        return lines

    @property
    def lines_temperature(self):
        lines = ['# Temperature', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
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
        lines = ['# Source Statistics', '']
        DELIM_COLUMN = ' | '
        keys = [
            'source_id',
            'n',
            'n_parse_attempted',
            'n_parse_successful',
            'min_date',
            'max_date',
        ]
        sep = ['---' for _ in keys]

        def build_row(values):
            return DELIM_COLUMN + DELIM_COLUMN.join(values) + DELIM_COLUMN

        lines.append(build_row(keys))
        lines.append(build_row(sep))
        for source_id, stats in source_to_stats.items():
            values = [str(stats.get(key, '')) for key in keys]
            lines.append(build_row([source_id] + values))
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

    def build_sub_readmes(self):
        links = []
        for id, lines in [
            ('temperature_by_city', self.lines_temperature),
            ('rainfall_by_city', self.lines_rainfall),
            ('data_coverage', self.lines_coverage),
            ('source_statistics', self.lines_source_stats),
        ]:
            readme_path = os.path.join(DIR_REPO, f'README.{id}.md')
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
