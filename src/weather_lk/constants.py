import os
import tempfile

import googlemaps

GIT_REPO_URL = 'https://github.com/nuuuwan/weather_lk'
DIR_REPO = os.path.join(tempfile.gettempdir(), 'weather_lk')
DIR_REPO_DAILY_DATA = os.path.join(DIR_REPO, 'daily_data')

BRANCH_NAME = 'data'

DIR_DATA_PLACE_TO_LATLNG = 'data_place_to_latlng'
PLACE_TO_LATLNG_PATH = os.path.join(
    DIR_DATA_PLACE_TO_LATLNG, 'place_to_latlng.json'
)
PLACE_TO_LATLNG_PATH_NEW = os.path.join(
    DIR_DATA_PLACE_TO_LATLNG, 'place_to_latlng.new.json'
)

GMAPS_API_KEY = os.environ.get('GMAPS_API_KEY')
GMAPS = googlemaps.Client(GMAPS_API_KEY) if GMAPS_API_KEY else None
DEFAULT_LATLNG = [0, 0]

DIR_DATA_BY_PLACE = os.path.join(DIR_REPO, 'data_by_place')