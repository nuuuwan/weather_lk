from functools import cached_property

from utils import JSONFile, Log

from weather_lk.constants import (DEFAULT_LATLNG, GMAPS, PLACE_TO_LATLNG_PATH,
                                  PLACE_TO_LATLNG_PATH_NEW)
from weather_lk.core.Data import Data
from weather_lk.core.NORMALIZED_NAME_IDX import NORMALIZED_NAME_IDX

log = Log('History')


class PlaceToLatLng:
    @cached_property
    def place_list(self):
        place_set = set()
        for place in Data().raw_place_list:
            place_set.add(NORMALIZED_NAME_IDX.get(place, place))
            place_set.add(place)
        return sorted(list(place_set))

    def build_place_to_latlng(self, place_to_latlng_old) -> dict:
        place_to_latlng = place_to_latlng_old
        for place in self.place_list:
            if place not in place_to_latlng:
                if (
                    place_to_latlng_old.get(place, DEFAULT_LATLNG)
                    != DEFAULT_LATLNG
                ):
                    place_to_latlng[place] = place_to_latlng_old[place]
                else:
                    latlng = PlaceToLatLng.get_latlng(place)
                    log.debug(f'{place} -> {latlng}')
                    place_to_latlng[place] = latlng
        place_to_latlng = dict(
            sorted(place_to_latlng.items(), key=lambda item: item[0])
        )
        return place_to_latlng

    @staticmethod
    def get_latlng(place: str):
        geocode_result = GMAPS.geocode(f'{place}, Sri Lanka')
        if not geocode_result:
            return DEFAULT_LATLNG
        d = geocode_result[0]['geometry']['location']
        return (d['lat'], d['lng'])

    @staticmethod
    def get_place_to_latlng():
        return JSONFile(PLACE_TO_LATLNG_PATH).read()

    def save_place_to_latlng(self):
        place_to_latlng_old = JSONFile(PLACE_TO_LATLNG_PATH).read()
        place_to_latlng = self.build_place_to_latlng(place_to_latlng_old)

        n = len(place_to_latlng.keys())
        JSONFile(PLACE_TO_LATLNG_PATH_NEW).write(place_to_latlng)
        log.info(f'Saved {n} places to {PLACE_TO_LATLNG_PATH_NEW}.')
        log.warn(f'Must be copied to {PLACE_TO_LATLNG_PATH}.')
