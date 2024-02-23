import re

from utils import Log

from weather_lk.meteo_gov_lk.REGEX import REGEX

log = Log('PDFParserClean')


class PDFParserClean:
    def clean_cell(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        return cell

    def clean_row(self, row):
        return [self.clean_cell(cell) for cell in row]

    def clean_location_name(self, cell):
        cell = re.sub(REGEX.NON_ASCII, '', cell)
        cell = re.sub(r'\s+', ' ', cell)
        cell = cell.strip()
        cell = cell.replace('wkqrdOmqrh', '')
        cell = cell.replace('polonnaruwa', 'Polonnaruwa')
        cell = cell.replace('Stations', ' ')
        cell = cell.replace('Station', ' ')
        cell = ' '.join(
            list(
                filter(
                    lambda word: len(word) > 0
                    and (word[0] != word[0].lower()),
                    cell.split(' '),
                )
            )
        )
        return cell
