import os

import matplotlib.pyplot as plt
from utils import TIME_FORMAT_TIME, Log, Time

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace

log = Log('ChartPlace')


class ChartPlace:
    N_ANNOTATE = 10

    def __init__(self, place, data_for_place):
        self.place = place
        self.data_for_place = data_for_place

    def set_text(self, ylabel):
        plt.title(self.place, fontsize=20)
        plt.xlabel('Date')
        plt.ylabel(ylabel)

        time_str = TIME_FORMAT_TIME.stringify(Time.now())
        footer_text = f'Generated at {time_str}'
        plt.figtext(0.5, 0.05, footer_text, ha='center', fontsize=8)

    @staticmethod
    def annotate(x, y_extreme, reverse, func_extreme, color, unit, gap_units):
        sorted_extreme_pairs = sorted(
            list(zip(x, y_extreme)),
            key=lambda x: x[1],
            reverse=reverse,
        )

        extreme = func_extreme(y_extreme)
        for i, [xi, yi] in enumerate(
            sorted_extreme_pairs[: ChartPlace.N_ANNOTATE]
        ):
            date_str = xi.strftime('%Y-%m-%d')
            caption = f'#{i+1} {yi:.1f}{unit} {date_str}'
            xy = (xi, yi)
            xytext = (xi, extreme - i * gap_units)
            plt.annotate(xy=xy, xytext=xytext, text=caption, color=color)

    def before_draw(self):
        plt.close()
        fig, ax = plt.subplots()

        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        for side in ['bottom', 'left', 'top', 'right']:
            ax.spines[side].set_visible(False)

        plt.grid(True, color='#eee')

    def after_draw(self):
        label = SummaryWriteDataByPlace.get_place_label(self.place)
        image_path = os.path.join(self.get_dir(), f'{label}.png')
        plt.savefig(image_path, dpi=300)
        plt.close()
        log.info(f'Wrote chart to {image_path}')

    def write(self):
        try:
            self.before_draw()
            self.draw()
            self.after_draw()
        except ValueError as e:
            log.error(f'{self.__class__}.write - {self.place}: {str(e)}')
