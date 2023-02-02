"""Tweet."""

from infograph import BarChart, DataTable, Infograph, RangeBarChart
from utils import Twitter


class WeatherReportTweeter:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    @property
    def tweet_image_path(self):
        return f'/tmp/weather_lk.{self.date_id}.png'

    def build_tweet_image(self):
        data_table = DataTable(self.weather_data.weather_list)
        infograph = Infograph(
            'Sri Lanka',
            'Temperature & Rainfall',
            self.weather_data.date,
            'meteo.gov.lk',
        )
        infograph.add(
            BarChart(
                'Rainfall (mm)',
                data_table['place'],
                data_table['rain'],
            )
        )
        infograph.add(
            RangeBarChart(
                'Rainfall (mm)',
                data_table['place'],
                data_table['min_temp'],
                data_table['max_temp'],
            )
        )
        infograph.write(self.tweet_image_path)

    @property
    def tweet_text(self):
        weather_data = self.weather_data
        max_temp = weather_data.max_temp
        min_temp = weather_data.min_temp
        max_rain = weather_data.max_rain
        return f'''Temperature & Rainfall ({weather_data.date}) by @MeteoLK

Rainfall 🌧️
😅 Highest: {max_rain.max_rain_place} ({max_rain.max_rain:.0f}mm)

Temperature 🌡️
🥵 Highest: {max_temp.max_temp_place} ({max_temp.max_temp_temp:.1f}°C)
🥶 Lowest: {min_temp.min_temp_place} ({min_temp.min_temp_temp:.1f}°C)

(24hrs ending at 8.30am)

#lka #SriLanka
        '''

    def tweet(self):
        Twitter.from_args().send(
            text=self.tweet_text,
            image_file_path_list=[self.tweet_image_path],
        )
