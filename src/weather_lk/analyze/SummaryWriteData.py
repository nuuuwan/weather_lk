import os

from utils import JSONFile, Log

from weather_lk.core.Data import Data
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

log = Log('SummaryWriteData')


class SummaryWriteData:
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
    N_ANNOTATE = 10

    @staticmethod
    def __write_json(label, x):
        summary_json_path = os.path.join(Data.DIR_REPO, f'{label}.json')
        JSONFile(summary_json_path).write(x)
        file_size_m = os.path.getsize(summary_json_path) / 1024 / 1024
        log.info(
            f'Wrote summary to {summary_json_path} ({file_size_m:.2f} MB)'
        )

    def write(self):
        SummaryWriteData.__write_json('list_all', Data.list_all())
        SummaryWriteData.__write_json('idx_by_place', Data.idx_by_place())
        SummaryWriteData.__write_json('idx_by_date', Data.idx_by_date())
