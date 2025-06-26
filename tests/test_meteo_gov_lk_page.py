import unittest

from weather_lk import MeteoGovLkPage


class TestCase(unittest.TestCase):
    def test_pdf_url(self):
        page = MeteoGovLkPage()
        pdf_url = page.pdf_url
        self.assertTrue("pdfs" in pdf_url)
        self.assertTrue("pdf" in pdf_url)
