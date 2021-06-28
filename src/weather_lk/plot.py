"""Plot."""

import matplotlib.pyplot as plt

from geo import geodata

from weather_lk._utils import log
from weather_lk import daily_weather_report


def _plot():
    _df = geodata.get_region_geodata('LK', 'district')
    log.info('Got geo data')

    data = daily_weather_report.daily_weather_report()
    log.info('Got weather data')

    _df.plot(
        column='area',
    )
    plt.show()

    Z = [[0, 0], [0, 1]]
    plt.contour(Z)
    plt.show()


if __name__ == '__main__':
    _plot()
