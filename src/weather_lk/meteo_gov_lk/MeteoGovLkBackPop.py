from functools import cached_property
from weather_lk.core.Data import Data
from weather_lk.constants import DIR_REPO_DAILY_DATA, DIR_REPO_METEO_GOV_LK_PDF
import os
from utils_future import RemotePDF
from utils import Log 

log = Log('MeteoGovLkBackPop')

class MeteoGovLkBackPop:
    @cached_property 
    def legacy_pdf_path_list(self):
        Data.init()
        pdf_path_list = []
        for file_name in os.listdir(DIR_REPO_DAILY_DATA):
            if not file_name.endswith('.pdf'):
                continue
            pdf_path = os.path.join(DIR_REPO_DAILY_DATA, file_name)
            pdf_path_list.append(pdf_path)
        return pdf_path_list
    
    def back_pop(self):
        for pdf_path in self.legacy_pdf_path_list:
            h32 = RemotePDF.file_hash(pdf_path)
            
            new_pdf_path = os.path.join(DIR_REPO_METEO_GOV_LK_PDF, f'{h32}.pdf')
            if not os.path.exists(new_pdf_path):
                os.rename(pdf_path, new_pdf_path)
                log.info(f'Wrote {new_pdf_path}')
            else:
                log.debug(f'{pdf_path} exists')


