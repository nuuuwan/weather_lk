"""Tweet."""


from utils import twitter

from weather_lk import daily_weather_report


def _hash(_s):
    return '#' + _s.replace(' ', '')


def _tweet():
    data = daily_weather_report.daily_weather_report()

    tweet_text = '''#SriLanka #Weather {date}
24hrs ending at 8.30am

🌧️ Rain
Highest: {max_rain_place} ({max_rain_rain:.0f}mm)

🌡️ Temperature
Highest: {max_temp_place} ({max_temp_temp:.1f}°C)
Lowest: {min_temp_place} ({min_temp_temp:.1f}°C)

#lka'''.format(
        date=data['date'],
        max_rain_place=_hash(data['max_rain']['place']),
        max_temp_place=_hash(data['max_temp']['place']),
        min_temp_place=_hash(data['min_temp']['place']),

        max_rain_rain=data['max_rain']['rain'],
        max_temp_temp=data['max_temp']['temp'],
        min_temp_temp=data['min_temp']['temp'],
    )

    print(tweet_text)
    print(len(tweet_text))


    twtr = twitter.Twitter.from_args()
    twtr.tweet(
        tweet_text=tweet_text,
        update_user_profile=True,
    )


if __name__ == '__main__':
    _tweet()
