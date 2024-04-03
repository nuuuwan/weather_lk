import os
from functools import cached_property

from utils import JSONFile, Log

from weather_lk.core import Data
from weather_lk.meteo_gov_lk.PDFParserGlobal import PDFParserGlobal
from weather_lk.meteo_gov_lk.PDFParserPlaceholder import PDFParserPlaceholder

log = Log('SummarySourceStats')


class SummarySourceStats:
    SOURCE_ID_MULTIPLE = 'multiple'
    SOURCE_ID_ALL = 'all'

    @staticmethod
    def get_file_stats(pdf_path):
        pdf_name = os.path.basename(pdf_path)
        file_id = pdf_name[:32]
        placeholder_path = PDFParserPlaceholder.get_placeholder_path(file_id)

        is_parse_attempted = False
        is_parse_successful = False
        date = None
        if os.path.exists(placeholder_path):
            is_parse_attempted = True
            placeholder_data = JSONFile(placeholder_path).read()
            data_path = placeholder_data['data_path']

            if 'json_parsed' in data_path:
                is_parse_successful = True
                date = placeholder_data['date']

        return dict(
            is_parse_attempted=is_parse_attempted,
            is_parse_successful=is_parse_successful,
            date=date,
        )

    @staticmethod
    def get_source_stats(pdf_paths):
        n = len(pdf_paths)
        n_parse_attempted = 0
        n_parse_successful = 0
        date_list = []
        for pdf_path in pdf_paths:
            file_stats = SummarySourceStats.get_file_stats(pdf_path)
            if file_stats['is_parse_attempted']:
                n_parse_attempted += 1
            if file_stats['is_parse_successful']:
                n_parse_successful += 1
            if file_stats['date']:
                date_list.append(file_stats['date'])

        min_date, max_date = None, None
        year_to_n = {}
        if date_list:
            date_list.sort()
            min_date = date_list[0]
            max_date = date_list[-1]

            for date in date_list:
                year = date[:4]
                if year not in year_to_n:
                    year_to_n[year] = 0
                year_to_n[year] += 1

        return dict(
            n=n,
            n_parse_attempted=n_parse_attempted,
            n_parse_successful=n_parse_successful,
            n_parse_failed=n_parse_attempted - n_parse_successful,
            min_date=min_date,
            max_date=max_date,
            year_to_n=year_to_n,
        )

    @cached_property
    def source_to_pdf_paths(self):
        source_to_file_name = PDFParserGlobal.source_to_file_name()

        file_name_to_source_set = {}
        for source_id, file_names in source_to_file_name.items():
            for file_name in file_names:
                if file_name not in file_name_to_source_set:
                    file_name_to_source_set[file_name] = set()
                file_name_to_source_set[file_name].add(source_id)

        source_to_pdf_paths = {
            SummarySourceStats.SOURCE_ID_ALL: [],
            SummarySourceStats.SOURCE_ID_MULTIPLE: [],
        }
        for source_id, file_names in source_to_file_name.items():
            dir = os.path.join(Data.DIR_REPO, source_id)
            for file_name in file_names:
                is_duplicate = len(file_name_to_source_set[file_name]) > 1
                pdf_path = os.path.join(dir, file_name)
                source_ext_id = (
                    SummarySourceStats.SOURCE_ID_MULTIPLE
                    if is_duplicate
                    else source_id
                )
                if source_ext_id not in source_to_pdf_paths:
                    source_to_pdf_paths[source_ext_id] = []
                source_to_pdf_paths[source_ext_id].append(pdf_path)
                source_to_pdf_paths[SummarySourceStats.SOURCE_ID_ALL].append(
                    pdf_path
                )

        return source_to_pdf_paths

    @cached_property
    def source_to_stats(self):
        source_to_stats = {}
        for (
            source_id,
            pdf_paths,
        ) in self.source_to_pdf_paths.items():
            source_to_stats[source_id] = SummarySourceStats.get_source_stats(
                pdf_paths
            )
        return source_to_stats
