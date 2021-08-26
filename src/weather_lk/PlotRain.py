"""Plot."""
import matplotlib.pyplot as plt
from infographics.Figure import Figure
from infographics.Infographic import Infographic
from utils import timex

from weather_lk import daily_weather_report


class PlotRain(Figure):
    def __init__(
        self,
        left_bottom=(0.1, 0.25),
        width_height=(0.8, 0.6),
        figure_text='',
        date_id=timex.get_date_id(),
    ):
        super().__init__(
            left_bottom=left_bottom,
            width_height=width_height,
            figure_text=figure_text,
        )
        self.date_id = date_id
        self.__data__ = PlotRain.__prep_data(self)

    def __prep_data(self):
        data = daily_weather_report.load(self.date_id)
        date = data['date']
        weather_list = sorted(
            list(
                filter(
                    lambda item: item.get('rain', None) is not None,
                    data['weather_list'],
                )
            ),
            key=lambda item: item['rain'],
        )

        places = list(
            map(
                lambda item: item['place'],
                weather_list,
            )
        )
        rains = list(
            map(
                lambda item: item['rain'],
                weather_list,
            )
        )

        return (
            places,
            rains,
            date,
        )

    def draw(self):
        super().draw()
        (
            places,
            rains,
            date,
        ) = self.__data__

        ax = plt.axes(self.left_bottom + self.width_height)
        ax.grid()
        ax.set_ylim([0, 200])
        barlist = plt.bar(places, rains, color='blue')
        for i, rain in enumerate(rains):
            if rain > 150:
                color = (0, 0, 0.5)
            elif rain > 100:
                color = (0, 0, 1.0)
            elif rain > 50:
                color = (0, 0.5, 1.0)
            elif rain > 25:
                color = (0.5, 0.5, 1.0)
            else:
                color = (0.5, 1.0, 1.0)

            barlist[i].set_color(color)

        plt.ylabel('Rain (mm)')
        plt.xticks(rotation=90)


def _plot(date_id):
    image_file = '/tmp/weather_lk.%s.rain.png' % date_id
    plot_temp = PlotRain(
        date_id=date_id,
    )

    data = daily_weather_report.load(date_id)
    date = data['date']

    Infographic(
        title='Rain (%s)' % date,
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
    date_id = timex.get_date_id()
    _plot(date_id)
