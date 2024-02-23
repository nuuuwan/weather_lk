"""Tweet."""

from twtr import Tweet, Twitter
from utils import Log, String

from weather_lk.core.Data import Data
from weather_lk.twitter.TweeterCharts import TweeterCharts

log = Log('Tweeter')


def hash(x):
    return '#' + String(x).camel


def temp_to_emoji(temp):
    emojis = ['🟣', '🔵', '🟢', '🟡', '🟠', '🔴', '🟤']
    i = int(temp / 5) - 1
    i = max(0, min(i, len(emojis) - 1))
    return emojis[i]


class Tweeter(TweeterCharts):
    def __init__(self):
        self.data = Data.max()

    @property
    def text_header(self):
        weather_data = self.data
        date = weather_data['date']
        return '\n'.join(
            [
                f'Rainfall & Temperature ({date}) by @MeteoLK',
            ]
        )

    @property
    def text_footer(self):
        return '\n'.join(
            [
                '(24hrs ending at 8.30am)',
                '#lka #SriLanka 🇱🇰',
            ]
        )

    @property
    def text_temp(self):
        weather_data = self.data
        min_temp_data = weather_data['min_temp']
        max_temp_data = weather_data['max_temp']
        min_temp = min_temp_data['min_temp']
        max_temp = max_temp_data['max_temp']
        min_temp_place = hash(min_temp_data['min_temp_place'])
        max_temp_place = hash(max_temp_data['max_temp_place'])
        max_temp_emoji = temp_to_emoji(max_temp)
        min_temp_emoji = temp_to_emoji(min_temp)

        return '\n'.join(
            [
                'Temperature 🌡️',
                f'{max_temp_emoji} Max: {max_temp:.1f}°C in {max_temp_place}',
                f'{min_temp_emoji} Min: {min_temp:.1f}°C in {min_temp_place}',
            ]
        )

    @property
    def text_rain(self):
        weather_data = self.data
        max_rain_data = weather_data['max_rain']
        max_rain = max_rain_data['max_rain']
        if max_rain < 0.5:
            return '⚠️ No rainfall recorded at any weather station.'
        max_rain_place = hash(max_rain_data['max_rain_place'])

        max_rain_inches = int(round(max_rain / 25.4, 0))
        max_rain_emoji = '💧' * max_rain_inches

        return '\n'.join(
            [
                'Rainfall 📏',
                f'🌧️ Max: {max_rain:.0f}mm '
                + f'in {max_rain_place} {max_rain_emoji}',
            ]
        )

    @property
    def tweet_text(self):
        return '\n'.join(
            [
                self.text_header,
                '',
                self.text_temp,
                '',
                self.text_rain,
                '',
                self.text_footer,
            ]
        )

    @property
    def tweet(self):
        text = self.tweet_text
        print(text)
        n_text = len(text)
        log.debug(f'{n_text=}')
        tweet_image_path = self.tweet_image_path
        log.debug(f'{tweet_image_path=}')
        return Tweet(text).add_image(tweet_image_path)

    def send(self):
        self.build_tweet_image()
        self.tweet

        try:
            twitter = Twitter()
            twitter.send()
        except Exception as e:
            log.error(f'Tweeter.send: {str(e)}')
