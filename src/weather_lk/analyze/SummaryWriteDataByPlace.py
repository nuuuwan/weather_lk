import os
from functools import cache

from utils import JSONFile, Log, TSVFile

from weather_lk.constants import DIR_DATA_BY_PLACE
from weather_lk.core.Data import Data
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

log = Log('SummaryWriteDataByPlace')


class SummaryWriteDataByPlace:
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
    N_ANNOTATE = 10

    @staticmethod
    @cache
    def get_place_label(place):
        lat, lng = SummaryWriteDataByPlace.PLACE_TO_LATLNG[place]
        place_id = place.replace(' ', '-')
        return f'{lng:.2f}E-{lat:.2f}N-{place_id}'

    @staticmethod
    def __write_for_place(place, data_for_place):
        label = SummaryWriteDataByPlace.get_place_label(place)
        n = len(data_for_place)

        json_path = os.path.join(DIR_DATA_BY_PLACE, f'{label}.json')
        JSONFile(json_path).write(data_for_place)

        tsv_path = os.path.join(DIR_DATA_BY_PLACE, f'{label}.tsv')
        TSVFile(tsv_path).write(data_for_place)

        log.info(f'Wrote {json_path}/tsv ({n} records)')

    def write_by_place(self):
        if not os.path.exists(DIR_DATA_BY_PLACE):
            os.makedirs(DIR_DATA_BY_PLACE)

        for place, data_for_place in Data.idx_by_place().items():
            try:
                SummaryWriteDataByPlace.__write_for_place(
                    place, data_for_place
                )
            except Exception as e:
                log.error(f'write_by_place - {place}: {str(e)}')
