"""Plot."""
import matplotlib.pyplot as plt
from infographics.Figure import Figure
from infographics.Infographic import Infographic
from utils import TIME_FORMAT_DATE_ID, Time

from weather_lk import daily_weather_report


class PlotTemp(Figure):
    def __init__(
        self,
        left_bottom=(0.1, 0.25),
        width_height=(0.8, 0.6),
        figure_text='',
        date_id=TIME_FORMAT_DATE_ID.stringify(Time()),
    ):
        super().__init__(
            left_bottom=left_bottom,
            width_height=width_height,
            figure_text=figure_text,
        )
        self.date_id = date_id
        self.__data__ = PlotTemp.__prep_data(self)

    def __prep_data(self):
        data = daily_weather_report.load(self.date_id)
        date = data['date']
        weather_list = sorted(
            list(
                filter(
                    lambda item: item.get('max_temp')
                    and item.get('min_temp'),
                    data['weather_list'],
                )
            ),
            key=lambda item: item['max_temp'],
        )

        places = list(
            map(
                lambda item: item['place'],
                weather_list,
            )
        )
        min_temps = list(
            map(
                lambda item: item['min_temp'],
                weather_list,
            )
        )
        max_temps = list(
            map(
                lambda item: item['max_temp'],
                weather_list,
            )
        )
        max_temps_minus_min = list(
            map(
                lambda item: item['max_temp'] - item['min_temp'],
                weather_list,
            )
        )

        return (
            places,
            min_temps,
            max_temps,
            max_temps_minus_min,
            date,
        )

    def draw(self):
        super().draw()
        (
            places,
            min_temps,
            max_temps,
            max_temps_minus_min,
            date,
        ) = self.__data__

        ax = plt.axes(self.left_bottom + self.width_height)
        ax.grid()
        plt.bar(places, min_temps, color='white')
        barlist = plt.bar(
            places, max_temps_minus_min, bottom=min_temps, color='r'
        )

        for i, max_temp in enumerate(max_temps):
            color = 'r'
            if max_temp > 35:
                color = (0.5, 0, 0)
            elif max_temp > 30:
                color = (1, 0, 0)
            elif max_temp > 25:
                color = (1, 0.5, 0)
            elif max_temp > 20:
                color = (0.5, 1, 0)
            elif max_temp > 15:
                color = (0, 1, 0)
            elif max_temp > 10:
                color = (0, 1, 0.5)
            else:
                color = (0, 0, 1)
            barlist[i].set_color(color)

        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=90)


def _plot(date_id):
    image_file = '/tmp/weather_lk.%s.temp.png' % date_id
    plot_temp = PlotTemp(
        date_id=date_id,
    )

    data = daily_weather_report.load(date_id)
    date = data['date']

    Infographic(
        title='Temperature (%s)' % date,
        subtitle='In Sri Lanka',
        footer_text='\n'.join(
            [
                'data from https://www.meteo.gov.lk',
                'visualization by @nuuuwan',
            ]
        ),
        children=[plot_temp],
        size=(8, 9),
    ).save(image_file)
    return image_file


if __name__ == '__main__':
    date_id = TIME_FORMAT_DATE_ID.stringify(Time())
    _plot(date_id)
