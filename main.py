import pathlib

from src.data_source import LocalFileDataSourceParser, S3DataSourceParser
from src.report_service import ReportService

path = pathlib.Path(__file__).parent / "datasets"

s3_ds = S3DataSourceParser()
local_ds = LocalFileDataSourceParser(path)
events = s3_ds.get_raw_events()

reports = ReportService(events).create_performance_reports()
print("Done!")
