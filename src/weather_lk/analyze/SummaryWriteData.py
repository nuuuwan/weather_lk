import os

from utils import JSONFile, Log

from weather_lk.core.Data import Data
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

log = Log("SummaryWriteData")


class SummaryWriteData:
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
    N_ANNOTATE = 10

    @staticmethod
    def __write_json(label, x):
        summary_json_path = os.path.join(Data.DIR_REPO, f"{label}.json")
        JSONFile(summary_json_path).write(x)
        file_size_m = os.path.getsize(summary_json_path) / 1024 / 1024
        log.info(
            f"Wrote summary to {summary_json_path} ({file_size_m:.2f} MB)"
        )

    @staticmethod
    def __write_list_all__(d_list):
        SummaryWriteData.__write_json("list_all", d_list)

    @staticmethod
    def __write_idx_by_place__():
        idx_by_place = Data.idx_by_place()
        SummaryWriteData.__write_json("idx_by_place", idx_by_place)

    @staticmethod
    def __write_idx_by_date__():
        idx_by_date = Data.idx_by_date()
        date_list = sorted(list(idx_by_date.keys()))
        SummaryWriteData.__write_json("idx_by_date", idx_by_date)
        SummaryWriteData.__write_json("date_list", date_list)

    @staticmethod
    def __write_latest_flat__(d_list):
        latest = d_list[-1]
        time_ut = latest["date_ut"]
        weather_list = latest["weather_list"]
        latest_flat = []
        latest_places = []
        for weather in weather_list:
            flat_item = {
                "id": weather["place"],
                "time_ut": time_ut,
                "rain_mm": weather["rain"],
                "temp_min_c": weather["min_temp"],
                "temp_max_c": weather["max_temp"],
            }
            latest_flat.append(flat_item)

            place_item = {
                "id": weather["place"],
                "lat_lng": [weather["lat"], weather["lng"]],
            }
            latest_places.append(place_item)

        SummaryWriteData.__write_json("latest_flat", latest_flat)
        SummaryWriteData.__write_json("latest_places", latest_places)

    @staticmethod
    def __write_flat__(d_list):
        id_to_latlng = {}
        flat = []
        for d in d_list:
            time_ut = d["date_ut"]
            weather_list = d["weather_list"]
            for weather in weather_list:
                flat_item = {
                    "id": weather["place"],
                    "time_ut": time_ut,
                    "rain_mm": weather["rain"],
                    "temp_min_c": weather["min_temp"],
                    "temp_max_c": weather["max_temp"],
                }
                flat.append(flat_item)

                id_to_latlng[weather["place"]] = [
                    weather["lat"],
                    weather["lng"],
                ]

        flat_places = [
            {
                "id": place,
                "lat_lng": lat_lng,
            }
            for place, lat_lng in sorted(
                id_to_latlng.items(), key=lambda x: (-x[1][0], x[1][1])
            )
        ]

        SummaryWriteData.__write_json("flat", flat)
        SummaryWriteData.__write_json("flat_places", flat_places)

    def write(self):
        d_list = Data.list_all()
        SummaryWriteData.__write_list_all__(d_list)
        SummaryWriteData.__write_idx_by_place__()
        SummaryWriteData.__write_idx_by_date__()
        SummaryWriteData.__write_latest_flat__(d_list)
        SummaryWriteData.__write_flat__(d_list)
