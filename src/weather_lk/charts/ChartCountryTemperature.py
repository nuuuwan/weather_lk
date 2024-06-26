from weather_lk.charts.ChartCountry import ChartCountry
from weather_lk.charts.ChartTemperature import ChartTemperature
from weather_lk.core import Data


class ChartCountryTemperature(ChartCountry, ChartTemperature):
    def get_label(self):
        return 'country_temperature'

    def get_dir(self):
        return Data.DIR_DATA_CHARTS

    def get_data(self):
        sorted_weather_list = self.sorted_weather_list
        x = [d['place'] for d in sorted_weather_list]
        y_min_temp = [d['min_temp'] for d in sorted_weather_list]
        y_max_temp = [d['max_temp'] for d in sorted_weather_list]

        # clean nulls
        x, y_min_temp, y_max_temp = zip(
            *[
                z
                for z in zip(x, y_min_temp, y_max_temp)
                if (z[1] is not None) and (z[2] is not None)
            ]
        )

        return x, y_min_temp, y_max_temp

    def get_title(self):
        date = self.data_latest['date']
        return f'Temperature ({date})'

    def draw(self):
        self.set_text('Temperature (°C)')
        x, y_min_temp, y_max_temp = self.get_data()
        self.set_ylim(y_min_temp, y_max_temp)
        ChartCountryTemperature.plot_bars(x, y_min_temp, y_max_temp)
        ChartCountryTemperature.annotate(
            x, y_max_temp, True, max, '#c00', '°C', 2
        )
        ChartCountryTemperature.annotate(
            x, y_min_temp, False, min, '#008', '°C', 2
        )


if __name__ == '__main__':
    image_path = ChartCountryTemperature().write()
