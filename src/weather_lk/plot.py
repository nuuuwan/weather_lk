"""Plot."""
import matplotlib.pyplot as plt

from weather_lk._utils import log
from weather_lk import daily_weather_report


def _plot_temp():
    data = daily_weather_report.daily_weather_report()
    date = data['date']
    weather_list = sorted(list(filter(
        lambda item: 'temp_max' in item,
        data['weather_list'],
    )), key=lambda item: item['temp_max'])

    places = list(map(
        lambda item: item['place'],
        weather_list,
    ))
    temp_mins = list(map(
        lambda item: item['temp_min'],
        weather_list,
    ))
    temp_maxs_minus_min = list(map(
        lambda item: item['temp_max'] - item['temp_min'],
        weather_list,
    ))

    ax = plt.gca()
    ax.grid()
    plt.bar(places, temp_mins, color='white')
    plt.bar(places, temp_maxs_minus_min, bottom=temp_mins, color='r')

    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=90)
    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.2)

    fig.set_size_inches((8, 9))
    date_id = date.replace('-', '')
    image_file = '/tmp/weather_lk.%s.temp.png' % date_id
    fig.savefig(image_file, dpi=300)
    log.info('Saved temperature plot to %s', image_file)
    plt.close()

    return image_file


def _plot_rain():
    data = daily_weather_report.daily_weather_report()
    date = data['date']
    weather_list = sorted(list(filter(
        lambda item: item.get('rain', None) is not None,
        data['weather_list'],
    )), key=lambda item: item['rain'])

    places = list(map(
        lambda item: item['place'],
        weather_list,
    ))

    rains = list(map(
        lambda item: item['rain'],
        weather_list,
    ))

    ax = plt.gca()
    ax.grid()
    plt.bar(places, rains, color='blue')
    plt.ylabel('Rain (mm)')
    plt.xticks(rotation=90, fontsize=8)
    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.15)

    fig.set_size_inches((8, 9))
    date_id = date.replace('-', '')
    image_file = '/tmp/weather_lk.%s.rain.png' % date_id
    fig.savefig(image_file, dpi=300)
    log.info('Saved temperature plot to %s', image_file)
    plt.close()

    return image_file


if __name__ == '__main__':
    _plot_temp()
    _plot_rain()
