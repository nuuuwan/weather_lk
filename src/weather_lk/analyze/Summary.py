from functools import cached_property
import os
import tempfile
from utils import Log, Git, JSONFile, TSVFile
from weather_lk.place_to_latlng.PlaceToLatLng import PlaceToLatLng

GIT_REPO_URL = 'https://github.com/nuuuwan/weather_lk'
DIR_REPO = os.path.join(tempfile.gettempdir(), 'weather_lk')
DIR_REPO_DAILY_DATA = os.path.join(DIR_REPO, 'daily_data')

BRANCH_NAME = 'data'

log = Log('Summary')


class Summary:
    DIR_DATA_BY_PLACE = 'data_by_place'
    PLACE_TO_LATLNG = PlaceToLatLng.get_place_to_latlng()
        
    
    @cached_property
    def data_by_place(self):
        idx = {}
        for data in self.data_list:
            date = data['date']
            for item in data['weather_list']:
                place = item['place']
                d = dict(
                    rain=item['rain'],
                    temp_min=item.get('temp_min', None),
                    temp_max=item.get('temp_max', None),
                    date = date
                )

                if place not in idx:
                    idx[place] = []
                idx[place].append(d)

        idx = dict(sorted(idx.items(), key=lambda x: x[0]))
        return idx

    @cached_property
    def data_list(self):
        git = Git(GIT_REPO_URL)
        git.clone(DIR_REPO)
        git.checkout(BRANCH_NAME)

        data_list = []
        for file_only in os.listdir(DIR_REPO_DAILY_DATA):
            if not (
                file_only.startswith('weather_lk.')
                and file_only.endswith('.json')
            ):
                continue
            file_path = os.path.join(DIR_REPO_DAILY_DATA, file_only)
            data = JSONFile(file_path).read()
            data_list.append(data)
        data_list = sorted(data_list, key=lambda x: x['date'])
        min_date = data_list[0]['date']
        max_date = data_list[-1]['date']
        
        n = len(data_list)
        log.info(f'Loaded data for {n:,} days, ' + f'from {min_date} to {max_date}.' )
        return data_list
    

    @staticmethod 
    def __write_json(label, x):
        summary_json_path = os.path.join(DIR_REPO, f'{label}.json')
        JSONFile(summary_json_path).write(x)
        file_size_m = os.path.getsize(summary_json_path) / 1024 / 1024
        log.info(f'Wrote summary to {summary_json_path} ({file_size_m:.2f} MB)')


    def write(self):
        Summary.__write_json('data_list',self.data_list)
        Summary.__write_json('data_by_place',self.data_by_place)

    @staticmethod
    def __write_for_place(place, data_for_place):
        lat, lng = Summary.PLACE_TO_LATLNG[place]
        place_id = place.replace(' ', '-')  
        label = f'{lng:.2f}E-{lat:.2f}N-{place_id}'
        n = len(data_for_place)

        json_path = os.path.join(Summary.DIR_DATA_BY_PLACE, f'{label}.json')
        JSONFile(json_path).write(data_for_place)
        
        tsv_path = os.path.join(Summary.DIR_DATA_BY_PLACE, f'{label}.tsv')
        TSVFile(tsv_path).write(data_for_place)
        log.info(f'Wrote data for {place} to {label}.* ({n} records)')


    def write_by_place(self):
        if not os.path.exists(Summary.DIR_DATA_BY_PLACE):
            os.makedirs(Summary.DIR_DATA_BY_PLACE)

        for place, data_for_place in self.data_by_place.items():
            try:
                Summary.__write_for_place(place, data_for_place)    
            except Exception as e:
                log.error(f'Error writing data for {place}: {str(e)}')
  