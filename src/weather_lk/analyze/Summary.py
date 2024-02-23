from utils import Log

from weather_lk.analyze.SummaryCoverage import SummaryCoverage
from weather_lk.analyze.SummaryDataCharts import SummaryDataCharts
from weather_lk.analyze.SummaryReadMe import SummaryReadMe
from weather_lk.analyze.SummaryWriteData import SummaryWriteData
from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace
from weather_lk.constants import TEST_MODE

log = Log('Summary')


class Summary(
    SummaryCoverage,
    SummaryDataCharts,
    SummaryWriteData,
    SummaryWriteDataByPlace,
    SummaryReadMe,
):
    def write_all(self):
        if not TEST_MODE:
            self.write()
            self.write_by_place()
            self.draw_charts_by_place()
            self.draw_charts_for_country()
            self.write_coverage()
            self.build_readme()
        else:
            self.draw_charts_by_place()
