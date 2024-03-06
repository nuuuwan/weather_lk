import os
from functools import cached_property

from utils import File, Log

from weather_lk.charts.ChartMinMaxPlot import ChartMinMaxPlot
from weather_lk.constants import (DIR_DATA_CHARTS,
                                  DIR_DATA_CHARTS_MIN_MAX_PLOT, DIR_REPO,
                                  DISPLAY_PLACES, TEST_MODE)
from weather_lk.core.Data import Data

log = Log('SummarySpecialCharts')


class SummarySpecialCharts:
    README_MIN_MAX_PLOT_PATH = os.path.join(
        DIR_REPO, 'README.min_max_plot.md'
    )

    @staticmethod
    def init():
        if not os.path.exists(DIR_DATA_CHARTS):
            os.makedirs(DIR_DATA_CHARTS)
        if not os.path.exists(DIR_DATA_CHARTS_MIN_MAX_PLOT):
            os.makedirs(DIR_DATA_CHARTS_MIN_MAX_PLOT)

    def draw_min_max_plot(self):
        SummarySpecialCharts.init()
        idx_by_place = Data.idx_by_place()
        readme_lines = []
        for place in DISPLAY_PLACES:
            if TEST_MODE and place != 'Colombo':
                continue
            data_for_place = idx_by_place.get(place, None)
            if data_for_place is None:
                log.warning(f'No data for {place}')
                continue

            ChartMinMaxPlot(place, data_for_place).write()
            readme_lines.extend(
                [
                    f'### {place}',
                    '',
                    f'![{place} Min Max Plot]({DIR_DATA_CHARTS_MIN_MAX_PLOT}/{place}.png)',
                    '',
                    '',
                ]
            )
        return readme_lines

    def build_min_max_plot_readme(self, lines_inner):
        lines = ['# Min Max Plots', ''] + lines_inner

        File(SummarySpecialCharts.README_MIN_MAX_PLOT_PATH).write_lines(lines)
        log.info(f'Wrote {SummarySpecialCharts.README_MIN_MAX_PLOT_PATH}')

    def build_min_max_plot(self):
        lines_inner = self.draw_min_max_plot()
        self.build_min_max_plot_readme(lines_inner)

    def build_special_charts(self):
        self.build_min_max_plot()

    @cached_property
    def lines_special_charts(self):
        return [
            '',
            '## Special Charts',
            '',
            f'* [Min Max Plot]({SummarySpecialCharts.README_MIN_MAX_PLOT_PATH})',
        ]
