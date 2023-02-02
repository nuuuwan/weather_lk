"""Tweet."""

from infograph import BarChart, DataTable, Infograph, RangeBarChart
from utils import String, Tweet, Twitter


def hash(x):
    return '#' + String(x).camel


def func_color_rain(_, yi):
    b = 1
    for limit, x in [
        [200, 1],
        [100, 2],
        [50, 3],
        [25, 4],
        [-1, 5],
    ]:
        if yi > limit:
            a = 1 / x
            g = 1 - 1 / x
            break

    r = g / 2
    return (r, g, b, a)


def func_color_temp(_, __, y2i):
    a = 0.5
    for limit, color in [
        [35, (0.5, 0, 0, a)],
        [30, (1, 0, 0, a)],
        [25, (1, 0.5, 0, a)],
        [20, (0, 1, 0, a)],
        [15, (0, 0.5, 1, a)],
        [10, (0, 0, 1, a)],
    ]:
        if y2i > limit:
            return color
    return (0, 0, 0.5, a)


class Tweeter:
    def __init__(self, weather_report):
        self.weather_report = weather_report

    @property
    def tweet_image_path(self):
        return f'/tmp/weather_lk.{self.weather_report.date_id}.png'

    def build_tweet_image(self):
        infograph = Infograph(
            'Sri Lanka',
            'Temperature & Rainfall',
            self.weather_report.weather_data['date'],
            'meteo.gov.lk',
        )

        data_table = DataTable(
            [
                d
                for d in self.weather_report.weather_list
                if d['rain'] is not None
            ],
        )
        data_table.sort('rain')
        infograph.add(
            BarChart(
                'Rainfall (mm)',
                data_table['place'],
                data_table['rain'],
                func_color_rain,
            )
        )

        data_table = DataTable(
            [
                d
                for d in self.weather_report.weather_list
                if d['min_temp'] is not None and d['max_temp'] is not None
            ],
        )
        data_table.sort('max_temp')
        infograph.add(
            RangeBarChart(
                'Rainfall (mm)',
                data_table['place'],
                data_table['min_temp'],
                data_table['max_temp'],
                func_color_temp,
            )
        )
        infograph.write(self.tweet_image_path)

    @property
    def tweet_text(self):
        weather_data = self.weather_report.weather_data
        weather_data['max_temp']
        min_temp = weather_data['min_temp']
        max_temp = weather_data['max_temp']
        max_rain = weather_data['max_rain']
        return f'''Temperature & Rainfall ({weather_data['date']}) by @MeteoLK

Rainfall 📏
🌧️ Max: {max_rain['max_rain']:.0f}mm in {hash(max_rain['max_rain_place'])}

Temperature 🌡️
🥵 Max: {max_temp['max_temp']:.1f}°C in {hash(max_temp['max_temp_place'])}
🥶 Min: {min_temp['min_temp']:.1f}°C in {hash(min_temp['min_temp_place'])}

(24hrs ending at 8.30am)

#lka #SriLanka
        '''

    @property
    def tweet(self):
        return Tweet(
            text=self.tweet_text,
            image_file_path_list=[self.tweet_image_path],
        )

    def send(self):
        self.build_tweet_image()
        Twitter.from_args().send(self.tweet)
