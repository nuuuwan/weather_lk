"""Daily Weather Report."""


from weather_lk.WeatherReportPDF import WeatherReportPDF

if __name__ == '__main__':
    WeatherReportPDF().download().parse()
