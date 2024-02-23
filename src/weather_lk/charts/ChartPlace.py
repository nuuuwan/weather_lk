import matplotlib.pyplot as plt
from utils import Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.charts.Chart import Chart

log = Log('ChartPlace')


class ChartPlace(Chart):
    N_ANNOTATE = 10

    def __init__(self, place, data_for_place):
        self.place = place
        self.data_for_place = data_for_place

    def get_title(self):
        return self.place + ' - History'

    def get_xlabel(self):
        return 'Date'

    @staticmethod
    def annotate(x, y_extreme, reverse, func_extreme, color, unit, gap_units):
        sorted_extreme_pairs = sorted(
            list(zip(x, y_extreme)),
            key=lambda x: x[1],
            reverse=reverse,
        )

        sign = -1 if reverse else 1

        extreme = func_extreme(y_extreme) - 5 * sign
        color_light = color + '2'
        for i, [xi, yi] in enumerate(
            sorted_extreme_pairs[: ChartPlace.N_ANNOTATE]
        ):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}{unit} {date_str}'
            xy = (xi, yi)
            xytext = (xi, extreme + i * sign * gap_units)
            plt.annotate(
                xy=xy,
                xytext=xytext,
                text=caption,
                color=color,
                arrowprops=dict(
                    facecolor=color_light,
                    width=0.25,
                    headwidth=5,
                    edgecolor=color_light,
                ),
                horizontalalignment='center',
                bbox=dict(facecolor=color_light, edgecolor='none', boxstyle="round"),
            )

    def get_label(self):
        return SummaryWriteDataByPlace.get_place_label(self.place)
