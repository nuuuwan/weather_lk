import camelot

from weather_lk._utils import log


class ParserMixin:
    @property
    def table_file_path(self):
        return self.file_path[:-4] + '.csv'

    @property
    def table(self):
        pdf_file = self.file_path
        tables = camelot.read_pdf(pdf_file, pages='all')
        tables.export(self.table_file_path, f='csv')
        log.info(f'Wrote {self.table_file_path}')
        table = tables[0].df.values.tolist()
        return table
