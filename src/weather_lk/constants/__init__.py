import os
import tempfile

import googlemaps

# ...

from weather_lk.constants.DISPLAY_PLACES import DISPLAY_PLACES

# ...

TEST_MODE = os.name == 'nt'

GIT_REPO_URL = 'https://github.com/nuuuwan/weather_lk'
DIR_REPO = os.path.join(tempfile.gettempdir(), 'weather_lk')


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
DIR_DATA_CHARTS = os.path.join(DIR_REPO, 'charts')
DIR_DATA_CHARTS_RAINFALL = os.path.join(DIR_DATA_CHARTS, 'rainfall')
DIR_DATA_CHARTS_TEMPERATURE = os.path.join(DIR_DATA_CHARTS, 'temperature')


URL_REMOTE_DATA = 'https://raw.githubusercontent.com/nuuuwan/weather_lk/data'

DIR_REPO_PDF_ARCHIVE_ORG = os.path.join(DIR_REPO, 'pdf_archive_org')
DIR_REPO_PDF_METEO_GOV_LK = os.path.join(DIR_REPO, 'pdf_meteo_gov_lk')
DIR_REPO_PDF_GOOGLE_SEARCH = os.path.join(DIR_REPO, 'pdf_google_search')
DIR_REPO_PDF_PARSED = os.path.join(DIR_REPO, 'pdf_parsed')

DIR_REPO_JSON_PARSED = os.path.join(DIR_REPO, 'json_parsed')
DIR_REPO_JSON_PLACEHOLDER = os.path.join(DIR_REPO, 'json_placeholder')

COVERAGE_WINDOW_LIST = [7, 28, 365, 3652]
CHART_WINDOWS = [None, 28, 91]

