import os
import tempfile
from functools import cache, cached_property

from utils import Git, JSONFile, Log

from weather_lk.core.NORMALIZED_NAME_IDX import NORMALIZED_NAME_IDX

log = Log('Data')


class Data:
    BRANCH_NAME = 'data'
    GIT_REPO_URL = 'https://github.com/nuuuwan/weather_lk'
    DIR_REPO = os.path.join(tempfile.gettempdir(), 'weather_lk')
    log.debug(f'{DIR_REPO=}')

    DIR_DATA_CHARTS = os.path.join(DIR_REPO, 'charts')
    DIR_DATA_BY_PLACE = os.path.join(DIR_REPO, 'data_by_place')
    DIR_DATA_CHARTS_MIN_MAX_PLOT = os.path.join(
        DIR_DATA_CHARTS, 'min_max_plot'
    )
    DIR_DATA_CHARTS_RAINFALL = os.path.join(DIR_DATA_CHARTS, 'rainfall')
    DIR_DATA_CHARTS_TEMPERATURE = os.path.join(DIR_DATA_CHARTS, 'temperature')

    DIR_REPO_PDF_ARCHIVE_ORG = os.path.join(DIR_REPO, 'pdf_archive_org')
    DIR_REPO_PDF_METEO_GOV_LK = os.path.join(DIR_REPO, 'pdf_meteo_gov_lk')
    DIR_REPO_PDF_GOOGLE_SEARCH = os.path.join(DIR_REPO, 'pdf_google_search')
    DIR_REPO_PDF_PARSED = os.path.join(DIR_REPO, 'pdf_parsed')
    DIR_REPO_JSON_PARSED = os.path.join(DIR_REPO, 'json_parsed')
    DIR_REPO_JSON_PLACEHOLDER = os.path.join(DIR_REPO, 'json_placeholder')

    @staticmethod
    def init():
        git = Git(Data.GIT_REPO_URL)
        if os.path.exists(Data.DIR_REPO):
            log.debug('Repo Exists. Not cloning.')
            return
        git.clone(Data.DIR_REPO, Data.BRANCH_NAME)
        git.checkout(Data.BRANCH_NAME)

    @staticmethod
    @cache
    def get_data_path_list():
        Data.init()
        data_path_list = []
        for file_name in os.listdir(Data.DIR_REPO_JSON_PARSED):
            if file_name.endswith('.json'):
                data_path = os.path.join(Data.DIR_REPO_JSON_PARSED, file_name)
                data_path_list.append(data_path)
        return data_path_list

    @staticmethod
    def clean(data):
        for place in NORMALIZED_NAME_IDX:
            normalized = NORMALIZED_NAME_IDX[place]
            for item in data['weather_list']:
                if item['place'] == place:
                    item['place'] = normalized
        return data

    @staticmethod
    def list_all_raw():
        data_path_list = Data.get_data_path_list()
        data_list = []
        for data_path in data_path_list:
            data = JSONFile(data_path).read()
            data_list.append(data)
        return data_list

    @staticmethod
    def list_all():
        data_list = Data.list_all_raw()
        cleaned_data_list = [Data.clean(data) for data in data_list]
        sorted_data_list = sorted(cleaned_data_list, key=lambda x: x['date'])
        return sorted_data_list

    @staticmethod
    def max():
        data_list = Data.list_all()
        return data_list[-1]

    @staticmethod
    def idx_by_date():
        data_list = Data.list_all()
        idx = {}
        for data in data_list:
            date = data['date']
            idx[date] = data
        return idx

    @staticmethod
    def idx_by_place():
        data_list = Data.list_all()
        idx = {}
        for data in data_list:
            weather_list = data['weather_list']
            for item in weather_list:
                place = item['place']
                if place not in idx:
                    idx[place] = []
                d = dict(
                    date=data['date'],
                    rain=item['rain'],
                    min_temp=item['min_temp'],
                    max_temp=item['max_temp'],
                )
                idx[place].append(d)

        idx = dict(sorted(idx.items(), key=lambda item: item[0]))
        return idx

    @cached_property
    def place_list(self):
        idx_by_place = Data.idx_by_place()
        place_and_n = [
            (place, len(idx_by_place[place])) for place in idx_by_place
        ]
        sorted_place_and_n = sorted(
            place_and_n, key=lambda x: x[1], reverse=True
        )
        return [place for place, __ in sorted_place_and_n]

    @cached_property
    def raw_place_list(self):
        data_list = Data.list_all_raw()
        place_set = set()
        for data in data_list:
            weather_list = data['weather_list']
            for item in weather_list:
                place = item['place']
                place_set.add(place)
        return sorted(list(place_set))


def main():
    idx = Data.idx_by_place()
    print(idx['Colombo'])


if __name__ == "__main__":
    main()
