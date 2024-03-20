from utils import Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.charts.Chart import Chart
from weather_lk.core.Data import Data

log = Log('ChartPlace')


class ChartPlace(Chart):
    def __init__(self, place, data_for_place, window=None):
        self.place = place
        self.data_for_place = data_for_place
        self.window = window

    def get_title(self):
        title = self.place
        data_latest = Data.max()
        date = data_latest['date']
        if self.window:
            title += f' - Last {self.window} days'
        title += f', as of {date}'
        return title

    def get_xlabel(self):
        return 'Date'

    def get_label(self):
        return SummaryWriteDataByPlace.get_place_label(self.place)
