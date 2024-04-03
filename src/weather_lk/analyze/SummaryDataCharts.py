import os

from utils import Log

from weather_lk.charts.ChartCountryRainfall import ChartCountryRainfall
from weather_lk.charts.ChartCountryTemperature import ChartCountryTemperature
from weather_lk.charts.ChartPlaceRainfall import ChartPlaceRainfall
from weather_lk.charts.ChartPlaceTemperature import ChartPlaceTemperature
from weather_lk.constants import DISPLAY_PLACES, TEST_MODE
from weather_lk.core.Data import Data

log = Log('SummaryDataCharts')


class SummaryDataCharts:
    CHART_WINDOWS = [None, 28, 91]
    N_ANNOTATE = 10

    @staticmethod
    def init():
        if not os.path.exists(Data.DIR_DATA_CHARTS):
            os.makedirs(Data.DIR_DATA_CHARTS)
        if not os.path.exists(Data.DIR_DATA_CHARTS_RAINFALL):
            os.makedirs(Data.DIR_DATA_CHARTS_RAINFALL)
        if not os.path.exists(Data.DIR_DATA_CHARTS_TEMPERATURE):
            os.makedirs(Data.DIR_DATA_CHARTS_TEMPERATURE)

    def draw_charts_by_place(self):
        SummaryDataCharts.init()

        idx_by_place = Data.idx_by_place()
        for place in DISPLAY_PLACES:
            if TEST_MODE and place != 'Colombo':
                continue
            data_for_place = idx_by_place.get(place, None)
            if data_for_place is None:
                log.warning(f'No data for {place}')
                continue

            for window in SummaryDataCharts.CHART_WINDOWS:
                ChartPlaceTemperature(
                    place, data_for_place, window=window
                ).write()
                ChartPlaceRainfall(
                    place, data_for_place, window=window
                ).write()

    def draw_charts_for_country(self):
        ChartCountryRainfall().write()
        ChartCountryTemperature().write()
