"""Utils."""
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('weather_lk')

logging.getLogger('pdfminer').setLevel(logging.WARNING)
logging.getLogger('camelot').setLevel(logging.WARNING)
