from utils import Log

from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.charts.Chart import Chart

log = Log('ChartPlace')


class ChartPlace(Chart):
    def __init__(self, place, data_for_place):
        self.place = place
        self.data_for_place = data_for_place

    def get_title(self):
        return self.place + ' - History'

    def get_xlabel(self):
        return 'Date'

    def get_label(self):
        return SummaryWriteDataByPlace.get_place_label(self.place)
