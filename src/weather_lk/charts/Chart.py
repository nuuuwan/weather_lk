import os

import matplotlib.pyplot as plt
from utils import Log
import matplotlib.pyplot as plt
from utils import TIME_FORMAT_TIME, Log, Time

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace




log = Log('Chart')


class Chart:

   

    def set_text(self, ylabel):
        plt.title(self.get_title(), fontsize=20)
        plt.xlabel(self.get_xlabel())
        plt.ylabel(ylabel)

        time_str = TIME_FORMAT_TIME.stringify(Time.now())
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
        ax.grid(True, which='major',linewidth=0.5, color='#888')

        plt.grid(True)

    def after_draw(self):
        label = self.get_label()
        image_path = os.path.join(self.get_dir(), f'{label}.png')
        plt.savefig(image_path, dpi=300)
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
