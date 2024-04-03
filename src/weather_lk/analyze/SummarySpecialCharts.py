import os
from functools import cached_property

from utils import File, Log

from weather_lk.analyze.SummaryReadMe import SummaryReadMe
from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.charts.ChartMinMaxPlot import ChartMinMaxPlot
from weather_lk.constants import DISPLAY_PLACES, TEST_MODE
from weather_lk.core.Data import Data

log = Log('SummarySpecialCharts')


class SummarySpecialCharts:
    README_MIN_MAX_PLOT_PATH = 'README.min_max_plot.md'

    @staticmethod
    def init():
        if not os.path.exists(Data.DIR_DATA_CHARTS):
            os.makedirs(Data.DIR_DATA_CHARTS)
        if not os.path.exists(Data.DIR_DATA_CHARTS_MIN_MAX_PLOT):
            os.makedirs(Data.DIR_DATA_CHARTS_MIN_MAX_PLOT)

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
            label = SummaryWriteDataByPlace.get_place_label(place)
            image_path_rain = (
                SummaryReadMe.URL_REMOTE_DATA
                + '/charts/min_max_plot/'
                + f'{label}.png'
            )
            readme_lines.extend(
                [
                    f'### {place}',
                    '',
                    f'![{place} Min Max Plot]({image_path_rain})',
                    '',
                    '',
                ]
            )
        return readme_lines

    def build_min_max_plot_readme(self, lines_inner):
        lines = ['# Min Max Plots', ''] + lines_inner

        readme_path = os.path.join(
            Data.DIR_REPO, SummarySpecialCharts.README_MIN_MAX_PLOT_PATH
        )
        File(readme_path).write_lines(lines)
        log.info(f'Wrote {readme_path}')

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
