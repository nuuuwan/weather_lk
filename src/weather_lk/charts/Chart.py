import datetime
import os

import matplotlib.pyplot as plt
from utils import Log, TimeFormat

log = Log('Chart')


class Chart:
    N_ANNOTATE = 3
    DPI = 300
    ROLLING_WINDOW = 7

    def set_text(self, ylabel):
        plt.title(self.get_title(), fontsize=20)
        plt.xlabel(self.get_xlabel())
        plt.ylabel(ylabel)

        time_str = TimeFormat.TIME.formatNow
        footer_text = f'Generated at {time_str}'
        plt.figtext(0.5, 0.05, footer_text, ha='center', fontsize=8)

    def before_draw(self):
        plt.close()
        fig, ax = plt.subplots()

        fig.autofmt_xdate()
        fig.set_size_inches(12, 6.75)

        for side in ['bottom', 'left', 'top', 'right']:
            ax.spines[side].set_visible(False)

        ax.grid(True, which='minor', linewidth=0.25, color='#ccc')
        ax.grid(True, which='major', linewidth=0.5, color='#888')

        plt.grid(True)

    def after_draw(self):
        label = self.get_label()
        if self.window:
            label += f'-{self.window}days'
        image_path = os.path.join(self.get_dir(), f'{label}.png')
        plt.savefig(image_path, dpi=Chart.DPI)
        plt.close()
        log.info(f'Wrote chart to {image_path}')

        return image_path

    def write(self):
        try:
            self.before_draw()
            self.draw()
            return self.after_draw()
        except ValueError as e:
            log.error(f'{self.__class__}.write - {self.place}: {str(e)}')

    @staticmethod
    def annotate_one(
        xi, yi, extreme, color, unit, gap_units, color_light, sign, i
    ):
        if yi == 0:
            return
        caption = f'#{i+1} {yi:.1f}{unit}'
        if isinstance(xi, datetime.datetime):
            date_str = xi.strftime('%Y-%m-%d')
            caption += f' ({date_str})'
        else:
            caption += f' ({xi})'

        plt.annotate(
            xy=(xi, yi),
            xytext=(xi, extreme + i * sign * gap_units),
            text=caption,
            color=color,
            bbox=dict(
                facecolor=color_light, edgecolor='none', boxstyle="round"
            ),
        )

    @classmethod
    def annotate(
        cls, x, y_extreme, reverse, func_extreme, color, unit, gap_units
    ):
        sorted_extreme_pairs = sorted(
            list(zip(x, y_extreme)),
            key=lambda x: x[1],
            reverse=reverse,
        )
        sign = -1 if reverse else 1
        extreme = func_extreme(y_extreme) - 5 * sign

        for i, [xi, yi] in enumerate(
            sorted_extreme_pairs[: Chart.N_ANNOTATE]
        ):
            color_light = cls.get_color(yi)
            Chart.annotate_one(
                xi, yi, extreme, color, unit, gap_units, color_light, sign, i
            )
