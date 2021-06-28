"""Plot."""
import math
import matplotlib.pyplot as plt
import numpy as np

from geo import geodata

from weather_lk._utils import log
from weather_lk import daily_weather_report


def _plot(
    title,
    field_key,
    cmap,
    levels,
):

    data = daily_weather_report.daily_weather_report()
    log.info('Got weather data')
    weather_list = data['weather_list']

    delta = 0.01

    X, Y, Z = [], [], []
    for lat in np.arange(5.9, 9.9, delta):
        x_row = []
        y_row = []
        z_row = []
        for lng in np.arange(79.5, 81.9, delta):
            x_row.append(lng)
            y_row.append(lat)

            inv_dis_sum = 0
            inv_dis_value_sum = 0
            for weather in weather_list:
                lat_lng = weather['lat_lng']
                if not lat_lng:
                    continue
                value = weather.get(field_key)
                if not value:
                    continue
                lat0, lng0 = lat_lng
                dis = math.pow(((lat0 - lat) ** 2 + (lng0 - lng) ** 2), 1)
                inv_dis = 1 / dis

                inv_dis_sum += inv_dis
                inv_dis_value_sum += inv_dis * value

            dis_value = inv_dis_value_sum / inv_dis_sum
            z_row.append(dis_value)

        X.append(x_row)
        Y.append(y_row)
        Z.append(z_row)

    fig, ax = plt.subplots()
    CS = ax.contourf(
        X, Y, Z,
        levels,
        cmap=cmap,
    )
    fig.colorbar(CS)
    ax.set_title(title)
    plt.axis('off')

    _df = geodata.get_region_geodata('LK', 'district')
    log.info('Got geo data')

    _df.plot(
        ax=ax,
        facecolor="none",
        edgecolor='black'
    )
    plt.show()




if __name__ == '__main__':
    # _plot(
    #     'Maxiumum Temperature (°C)',
    #     'temp_max',
    #     'coolwarm',
    #     [0, 5, 10, 15, 20, 25, 30, 35, 40],
    # )
    _plot(
        'Rainfall (mm)',
        'rain',
        'Blues',
        [0, 10, 20, 50, 100],
    )
