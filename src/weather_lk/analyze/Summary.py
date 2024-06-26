from utils import Log

from weather_lk.analyze.SummaryCoverage import SummaryCoverage
from weather_lk.analyze.SummaryDataCharts import SummaryDataCharts
from weather_lk.analyze.SummaryReadMe import SummaryReadMe
from weather_lk.analyze.SummarySourceStats import SummarySourceStats
from weather_lk.analyze.SummarySpecialCharts import SummarySpecialCharts
from weather_lk.analyze.SummaryWriteData import SummaryWriteData
from weather_lk.analyze.SummaryWriteDataByPlace import SummaryWriteDataByPlace

log = Log('Summary')


class Summary(
    SummaryCoverage,
    SummaryDataCharts,
    SummaryWriteData,
    SummaryWriteDataByPlace,
    SummaryReadMe,
    SummarySourceStats,
    SummarySpecialCharts,
):
    def write_all(self):
        self.write()
        self.write_by_place()
        self.draw_charts_by_place()
        self.draw_charts_for_country()
        self.build_special_charts()
        self.write_coverage()
        self.build_readme()
