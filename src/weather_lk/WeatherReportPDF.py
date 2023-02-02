from weather_lk.WeatherReportPDFDownloaderMixin import (
    WeatherReportPDFDownloaderMixin,
)
from weather_lk.WeatherReportPDFLoaderMixin import WeatherReportPDFLoaderMixin
from weather_lk.WeatherReportPDFParserMixin import WeatherReportPDFParserMixin
from weather_lk.WeatherReportPDFWeatherListParserMixin import (
    WeatherReportPDFWeatherListParserMixin,
)


class WeatherReportPDF(
    WeatherReportPDFDownloaderMixin,
    WeatherReportPDFLoaderMixin,
    WeatherReportPDFParserMixin,
    WeatherReportPDFWeatherListParserMixin,
):
    pass
