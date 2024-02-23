from weather_lk.meteo_gov_lk.PDFParserClean import PDFParserClean
from weather_lk.meteo_gov_lk.PDFParserExpandedData import PDFParserExpandedData
from weather_lk.meteo_gov_lk.PDFParserGlobal import PDFParserGlobal
from weather_lk.meteo_gov_lk.PDFParserParse import PDFParserParse
from weather_lk.meteo_gov_lk.PDFParserPlaceholder import PDFParserPlaceholder


class PDFParser(
    PDFParserClean,
    PDFParserParse,
    PDFParserExpandedData,
    PDFParserPlaceholder,
    PDFParserGlobal,
):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
