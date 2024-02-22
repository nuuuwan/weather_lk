"""Daily Weather Report."""


from weather_lk import Summary, Tweeter, WeatherReport

if __name__ == '__main__':
    weather_report = WeatherReport()
    weather_report.download()

    s = Summary()
    s.write()
    s.write_by_place()

    tweeter = Tweeter(weather_report)
    tweeter.send()
