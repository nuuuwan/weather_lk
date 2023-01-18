"""Utils."""
import logging

from utils import Log

logging.basicConfig(level=logging.INFO)
logging.getLogger('pdfminer').setLevel(logging.WARNING)
logging.getLogger('camelot').setLevel(logging.WARNING)

log = Log('weather_lk')
