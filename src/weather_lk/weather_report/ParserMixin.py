import camelot


class ParserMixin:
    @property
    def table(self):
        pdf_file = self.file_path
        tables = camelot.read_pdf(pdf_file, pages='all')
        table = tables[0].df.values.tolist()
        return table
