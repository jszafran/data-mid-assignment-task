import os
from unittest import TestCase

from src.db import DBManager
from src.types import ArticlePerformance, UserPerformance


class TestReportLoading(TestCase):
    def setUp(self) -> None:
        self.session = DBManager(os.getenv("DB_CONNECTION_STRING")).session

    def test_report_loading(self):
        self.assertEqual(0, self.session.query(ArticlePerformance).count())
        self.assertEqual(0, self.session.query(UserPerformance).count())
