"""Constants."""
CACHE_NAME, CACHE_TIMEOUT = 'weather_lk', 3600

URL = 'https://www.meteo.gov.lk/index.php?lang=en'
REGEX_DATE_URL = r'.+(?P<date_y>\d{4})-(?P<date_m>\d{2})-(?P<date_d>\d{2}).+'

REGEX_TEMP = r'(?P<temp>\d{2}\.\d{1})'
REGEX_DATE = r'(?P<date_str>\d{4}\.\d{2}\.\d{2})'
REGEX_PLACE_TEMP_RAIN = r'(?P<place>([A-Z][a-z]+\s*)+)' \
    + r' (?P<max_temp_str>((\d+\.\d+)+|NA|TR))' \
    + r' (?P<min_temp_str>((\d+\.\d+)+|NA|TR))' \
    + r' (?P<rain_str>((\d+\.\d+)+|NA|TR))'
REGEX_PLACE_RAIN_2 = r'(?P<place1>([A-Z][a-z]+\s*)+)' \
    + r' (?P<rain1_str>((\d+\.\d+)+|NA|TR))' \
    + r' (?P<place2>([A-Z][a-z]+\s*)+)' \
    + r' (?P<rain2_str>((\d+\.\d+)+|NA|TR))'
REGEX_HIGHEST = r'(?P<rain_str>((\d+\.\d+)+|NA|TR)) mm' \
    + r' (?P<place>([A-Z][a-z]+\s*)+)'
REGEX_NON_ASCII = r'[^\x00-\x7F]+'
