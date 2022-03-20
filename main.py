import pathlib

from src.data_source import LocalFileDataSourceParser, S3DataSourceParser
from src.db import DBManager
from src.report_service import ReportService

path = pathlib.Path(__file__).parent / "datasets"

s3_ds = S3DataSourceParser()
local_ds = LocalFileDataSourceParser(path)
events = s3_ds.get_raw_events()

reports = ReportService(events).create_performance_reports()

db_manager = DBManager("postgresql://user:password@postgres:5432/database")
db_manager.load_report(reports.article_performance_report)
db_manager.load_report(reports.user_performance_report)

print("Done!")
