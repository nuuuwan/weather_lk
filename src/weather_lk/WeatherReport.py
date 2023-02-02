from weather_lk.DownloaderMixin import DownloaderMixin
from weather_lk.LoaderMixin import LoaderMixin
from weather_lk.ParserMixin import ParserMixin
from weather_lk.WeatherListParserMixin import WeatherListParserMixin


class WeatherReport(
    DownloaderMixin,
    LoaderMixin,
    ParserMixin,
    WeatherListParserMixin,
):
    pass
