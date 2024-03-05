import os

from fuzzywuzzy import fuzz
from utils import File, Log

from weather_lk import Data

NORMALIZED_NAME_IDX = os.path.join(
    'src', 'weather_lk', 'core', 'NORMALIZED_NAME_IDX.py'
)
SCORE_THRESHOLD = 85
log = Log('build_normalized_place_idx')

OFFICIAL_PLACE_LIST = [
    'Hambantota',
    'Katugastota',
    'Kurunegala',
    'Maha Illuppallama',
    'Mattala',
    'Moneragala',
    'Mullaitivu',
    'Pottuvil',
    'Ratmalana',
    'Ratnapura',
    'Wellawaya',
]


def main():
    data_place_list = Data().raw_place_list
    place_list = OFFICIAL_PLACE_LIST + [
        place for place in data_place_list if place not in OFFICIAL_PLACE_LIST
    ]
    n = len(place_list)
    log.debug(f'{n=}')
    idx = {}
    for i in range(n - 1):
        place_i = place_list[i]
        for j in range(i + 1, n):
            place_j = place_list[j]
            if place_i == place_j:
                continue

            score = fuzz.ratio(place_i, place_j)
            if score >= SCORE_THRESHOLD:
                
                if place_j not in idx:
                    idx[place_j] = (place_i, score)
                    log.info(f'{place_j} -> {place_i} ({score})')
                else:
                    log.debug(f'{place_j} -> {place_i} ({score})')
            
    lines = ['# Auto Generated', 'NORMALIZED_NAME_IDX = {']
    for place, (normalized, score) in idx.items():
        lines.append(f'    "{place}": "{normalized}",  # {score}')
    lines.append('}')

    File(NORMALIZED_NAME_IDX).write_lines(lines)
    log.info(f'Wrote {NORMALIZED_NAME_IDX}')


if __name__ == "__main__":
    main()
