import os

from utils import Git, JSONFile, Log

from weather_lk.constants import (BRANCH_NAME, DIR_REPO, DIR_REPO_JSON_PARSED,
                                  GIT_REPO_URL)

log = Log('Data')


class Data:
    @staticmethod
    def init():
        git = Git(GIT_REPO_URL)
        git.clone(DIR_REPO)
        git.checkout(BRANCH_NAME)

    @staticmethod
    def get_data_path_list():
        Data.init()
        
        data_path_list = []
        for file_name in os.listdir(DIR_REPO_JSON_PARSED):
            if file_name.endswith('.json'):
                data_path = os.path.join(DIR_REPO_JSON_PARSED, file_name)
                data_path_list.append(data_path)
        return data_path_list

    @staticmethod
    def list_all():
        data_path_list = Data.get_data_path_list()
        data_list = []
        for data_path in data_path_list:
            data = JSONFile(data_path).read()
            data_list.append(data)

        sorted_data_list = sorted(data_list, key=lambda x: x['date'])
        log.info(f'Found {len(data_list)} data files.')
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


def main():
    idx = Data.idx_by_place()
    print(idx['Colombo'])


if __name__ == "__main__":
    main()
