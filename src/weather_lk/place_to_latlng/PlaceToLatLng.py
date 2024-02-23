import os
from functools import cached_property

from utils import Git, JSONFile, Log

from weather_lk.constants import (BRANCH_NAME, DEFAULT_LATLNG, DIR_REPO,
                                  DIR_REPO_JSON_PARSED, GIT_REPO_URL, GMAPS,
                                  PLACE_TO_LATLNG_PATH,
                                  PLACE_TO_LATLNG_PATH_NEW)

log = Log('History')


class PlaceToLatLng:
    @cached_property
    def history_list(self) -> list:
        self.git = Git(GIT_REPO_URL)
        self.git.clone(DIR_REPO)
        self.git.checkout(BRANCH_NAME)

        history_list = []
        for file_only in os.listdir(DIR_REPO_JSON_PARSED):
            if not (
                file_only.startswith('weather_lk.')
                and file_only.endswith('.json')
            ):
                continue
            file_path = os.path.join(DIR_REPO_JSON_PARSED, file_only)
            data = JSONFile(file_path).read()
            date = data['date']
            weather_list = data['weather_list']
            history_list.append(dict(date=date, weather_list=weather_list))
        n = len(history_list)
        log.info(f'Loaded data for {n} days.')
        return history_list

    def build_place_to_latlng(self, place_to_latlng_old) -> dict:
        place_to_latlng = {}
        for history in self.history_list:
            for weather in history['weather_list']:
                place = weather['place']
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
        log.info(f'Saved {n} places to {PLACE_TO_LATLNG_PATH}.')
