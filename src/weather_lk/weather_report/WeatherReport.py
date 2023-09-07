from weather_lk.weather_report.DownloaderMixin import DownloaderMixin
from weather_lk.weather_report.LoaderMixin import LoaderMixin
from weather_lk.weather_report.ParserMixin import ParserMixin
from weather_lk.weather_report.WeatherDataParserMixin import \
    WeatherDataParserMixin
from weather_lk.weather_report.WeatherListParserMixin import \
    WeatherListParserMixin


class WeatherReport(
    DownloaderMixin,
    LoaderMixin,
    ParserMixin,
    WeatherListParserMixin,
    WeatherDataParserMixin,
):
    pass
