"""Tweet."""


from utils import timex, twitter

from weather_lk import PlotRain, PlotTemp, daily_weather_report


def _hash(_s):
    return '#' + _s.replace(' ', '')


def _tweet():
    date_id = timex.get_date_id()
    data = daily_weather_report._load(date_id)

    if data['max_rain']['rain'] >= 0.1 and False:
        rain_str = '''Highest: {max_rain_place} ({max_rain_rain:.1f}mm)'''.format(
            max_rain_place=_hash(data['max_rain']['place']),
            max_rain_rain=data['max_rain']['rain'],
        )
    else:
        rain_str = 'No rain recorded islandwide.'

    tweet_text = '''Temperature & Rainfall ({date}) by @MeteoLK

Rainfall 🌧️
😅 {rain_str}

Temperature 🌡️
🥵 Highest: {max_temp_place} ({max_temp_temp:.1f}°C)
🥶 Lowest: {min_temp_place} ({min_temp_temp:.1f}°C)

(24hrs ending at 8.30am)

#lka #SriLanka'''.format(
        date=data['date'],
        max_temp_place=_hash(data['max_temp']['place']),
        min_temp_place=_hash(data['min_temp']['place']),
        max_temp_temp=data['max_temp']['temp'],
        min_temp_temp=data['min_temp']['temp'],
        rain_str=rain_str,
    )

    status_image_files = [
        PlotTemp._plot(date_id),
        PlotRain._plot(date_id),
    ]

    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        status_image_files=status_image_files,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
