"""Tweet."""


from utils import twitter, timex

from weather_lk import daily_weather_report
from weather_lk import plot


def _hash(_s):
    return '#' + _s.replace(' ', '')


def _tweet():
    date_id = timex.get_date_id()
    data = daily_weather_report._load(date_id)

    tweet_text = '''Temperature & Rainfall ({date}) by @MeteoLK

🌧️ Rainfall
Highest: {max_rain_place} ({max_rain_rain:.0f}mm)

🌡️ Temperature
Highest: {max_temp_place} ({max_temp_temp:.1f}°C)
Lowest: {min_temp_place} ({min_temp_temp:.1f}°C)

(24hrs ending at 8.30am)

#lka #SriLanka'''.format(
        date=data['date'],

        max_rain_place=_hash(data['max_rain']['place']),
        max_temp_place=_hash(data['max_temp']['place']),
        min_temp_place=_hash(data['min_temp']['place']),

        max_rain_rain=data['max_rain']['rain'],
        max_temp_temp=data['max_temp']['temp'],
        min_temp_temp=data['min_temp']['temp'],
    )

    status_image_files = [
        plot._plot_temp(date_id),
        plot._plot_rain(date_id),
    ]

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=status_image_files,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
