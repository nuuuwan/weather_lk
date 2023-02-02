"""Daily Weather Report."""


from weather_lk import Tweeter, WeatherReport

if __name__ == '__main__':
    weather_report_pdf = WeatherReport()
    weather_report_pdf.download()

    tweeter = Tweeter(weather_report_pdf.weather_data)
    tweeter.tweet()
