class REGEX:
    DATE_URL = r'.+(?P<date_y>\d{4})-(?P<date_m>\d{2})-(?P<date_d>\d{2}).+'

    TEMP = r'(?P<temp>\d{2}\.\d{1})'
    DATE = r'(?P<date_str>\d{4}\.\d{2}\.\d{2})'
    PLACE_TEMP_RAIN = (
        r'(?P<place>([A-Z][a-z]+\s*)+)'
        + r' (?P<max_temp_str>((\d+\.\d+)+|NA|TR))'
        + r' (?P<min_temp_str>((\d+\.\d+)+|NA|TR))'
        + r' (?P<rain_str>((\d+\.\d+)+|NA|TR))'
    )
    PLACE_RAIN_2 = (
        r'(?P<place1>([A-Z][a-z]+\s*)+)'
        + r' (?P<rain1_str>((\d+\.\d+)+|NA|TR))'
        + r' (?P<place2>([A-Z][a-z]+\s*)+)'
        + r' (?P<rain2_str>((\d+\.\d+)+|NA|TR))'
    )
    HIGHEST = (
        r'(?P<rain_str>((\d+\.\d+)+|NA|TR)) mm'
        + r' (?P<place>([A-Z][a-z]+\s*)+)'
    )
    NON_ASCII = r'[^\x00-\x7F]+'
