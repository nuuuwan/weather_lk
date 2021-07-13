"""Plot."""
import matplotlib.pyplot as plt
from infographics.Figure import Figure
from infographics.Infographic import Infographic
from utils import timex

from weather_lk import daily_weather_report


class PlotTemp(Figure):
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
        self.__data__ = PlotTemp.__prep_data(self)

    def __prep_data(self):
        data = daily_weather_report._load(self.date_id)
        date = data['date']
        weather_list = sorted(
            list(
                filter(
                    lambda item: 'temp_max' in item,
                    data['weather_list'],
                )
            ),
            key=lambda item: item['temp_max'],
        )

        places = list(
            map(
                lambda item: item['place'],
                weather_list,
            )
        )
        temp_mins = list(
            map(
                lambda item: item['temp_min'],
                weather_list,
            )
        )
        temp_maxs_minus_min = list(
            map(
                lambda item: item['temp_max'] - item['temp_min'],
                weather_list,
            )
        )

        return (
            places,
            temp_mins,
            temp_maxs_minus_min,
            date,
        )

    def draw(self):
        super().draw()
        (
            places,
            temp_mins,
            temp_maxs_minus_min,
            date,
        ) = self.__data__

        ax = plt.axes(self.left_bottom + self.width_height)
        ax.grid()
        plt.bar(places, temp_mins, color='white')
        plt.bar(places, temp_maxs_minus_min, bottom=temp_mins, color='r')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=90)


def _plot(date_id):
    image_file = '/tmp/weather_lk.%s.temp.png' % date_id
    plot_temp = PlotTemp(
        date_id=date_id,
    )

    data = daily_weather_report._load(date_id)
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
    date_id = timex.get_date_id()
    _plot(date_id)
