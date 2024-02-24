import os
from functools import cached_property

from utils import JSONFile, Log

from weather_lk.meteo_gov_lk.PDFParserGlobal import PDFParserGlobal
from weather_lk.meteo_gov_lk.PDFParserPlaceholder import PDFParserPlaceholder

log = Log('SummarySourceStats')


class SummarySourceStats:
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
        if date_list:
            date_list.sort()
            min_date = date_list[0]
            max_date = date_list[-1]
        return dict(
            n=n,
            n_parse_attempted=n_parse_attempted,
            n_parse_successful=n_parse_successful,
            min_date=min_date,
            max_date=max_date,
        )

    @cached_property
    def source_to_stats(self):
        source_to_stats = {}
        for (
            source_id,
            pdf_paths,
        ) in PDFParserGlobal.source_to_pdf_paths().items():
            source_to_stats[source_id] = SummarySourceStats.get_source_stats(
                pdf_paths
            )
        return source_to_stats
