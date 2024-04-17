import os

from utils import File, Log

from utils_future import Markdown
from weather_lk.analyze.SummaryCoverage import SummaryCoverage
from weather_lk.analyze.SummaryDataCharts import SummaryDataCharts
from weather_lk.analyze.SummaryMonthTrend import SummaryMonthTrend
from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import DISPLAY_PLACES
from weather_lk.core import Data

log = Log('SummaryReadMe')


class SummaryReadMe:
    URL_REMOTE_DATA = (
        'https://raw.githubusercontent.com/nuuuwan/weather_lk/data'
    )

    @property
    def lines_country(self):
        lines = []
        lines.extend(
            [
                '## Weather Nationwide :sri_lanka:',
                '',
                f'![Temperature]({SummaryReadMe.URL_REMOTE_DATA}'
                + '/charts/country_temperature.png)',
                '',
                f'![Rainfall]({SummaryReadMe.URL_REMOTE_DATA}/charts/country_rainfall.png)',
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
                SummaryReadMe.URL_REMOTE_DATA
                + '/charts/temperature/'
                + f'{label}.png'
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

    def get_lines_rainfall(self, window):
        title = 'Rainfall'
        if window:
            title += f' (Last {window} days)'
        lines = [f'# {title}', '']
        for place in DISPLAY_PLACES:
            label = SummaryWriteDataByPlace.get_place_label(place)
            if window:
                label += f'-{window}days'
            image_path_rain = (
                SummaryReadMe.URL_REMOTE_DATA
                + '/charts/rainfall/'
                + f'{label}.png'
            )
            lines.extend(
                [
                    f'## {place} ☔',
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

        for window in SummaryCoverage.COVERAGE_WINDOW_LIST:
            lines.extend(
                [
                    f'### Last {window:,} days',
                    '',
                    f'![Coverage]({SummaryReadMe.URL_REMOTE_DATA}/coverage-{window}days.png)',
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
        return ['# Source Statistics', ''] + Markdown.build_table(
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
        return ['', '## By Year', ''] + Markdown.build_table(
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

    @property
    def lines_month_trend(self):
        lines = ['# Trends by Month', '']
        for place in DISPLAY_PLACES:
            s = SummaryMonthTrend(place)

            lines.extend(s.md_table)
        return lines

    def build_sub_readmes(self):
        links = []

        temperature_infos = []
        rainfall_infos = []
        for window in SummaryDataCharts.CHART_WINDOWS:
            suffix = ''
            if window:
                suffix += f'_(last_{window}_days)'

            temperature_info = [
                'temperature_by_city' + suffix,
                self.get_lines_temperature(window),
            ]
            temperature_infos.append(temperature_info)

            rainfall_info = [
                'rainfall_by_city' + suffix,
                self.get_lines_rainfall(window),
            ]
            rainfall_infos.append(rainfall_info)

        for id, lines in (
            temperature_infos
            + rainfall_infos
            + [
                ('data_coverage', self.lines_coverage),
                (
                    'source_statistics',
                    self.lines_source_stats
                    + self.lines_source_stats_year_to_n,
                ),
                ('trend_by_month', self.lines_month_trend),
            ]
        ):
            readme_path = os.path.join(Data.DIR_REPO, f'README.{id}.md')
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
            + self.lines_special_charts
        )
        readme_path = os.path.join(Data.DIR_REPO, 'README.md')
        File(readme_path).write_lines(lines)
        log.info(f'Wrote README to {readme_path}')
