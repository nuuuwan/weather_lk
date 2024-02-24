import os
from weather_lk import PDFParser


if __name__ == "__main__":
    TEST_PDF_PATH = os.path.join('tests', 'data', '20240223.pdf')
    parser = PDFParser(TEST_PDF_PATH)
    parser.write_json()
