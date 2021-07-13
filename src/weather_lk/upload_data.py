"""Upload data to weather_lk:data branch."""

from weather_lk import daily_weather_report

if __name__ == '__main__':
    daily_weather_report._dump_latest()
