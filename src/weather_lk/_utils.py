"""Utils."""
import logging

from utils import jsonx, dt

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('weather_lk')


place_to_latlng = jsonx.read('src/weather_lk/assets/place-to-latlng.json')


def _get_location(place):
    if place in place_to_latlng:
        lat, lng = place_to_latlng[place]
        return round(lat, 4), round(lng, 4)
    return None


def _parse_float(float_str):
    if float_str == 'NA':
        return None
    return dt.parse_float(float_str)
