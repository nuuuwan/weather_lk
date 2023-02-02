"""Daily Weather Report."""


from weather_lk import Tweeter, WeatherReport

if __name__ == '__main__':
    weather_report = WeatherReport()
    weather_report.download()

    tweeter = Tweeter(weather_report)
    tweeter.send()
