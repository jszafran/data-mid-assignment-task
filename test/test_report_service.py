from unittest import TestCase

from src.report_service import ReportService
from src.types import (
    ArticlePerformanceReport,
    ReportServiceResult,
    UserPerformanceReport,
)


class TestReportService(TestCase):
    def test_if_irrelevant_events_are_skipped(self):
        raw_events = [
            {
                "TIMESTAMP": "2019-02-15 03:07:03.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "article_closed",
                "MD5(USER_ID)": "d09d39006ee0b4588c4db9545bfccd5e",
                "ATTRIBUTES": '{    "category": "digital_life",    "id": "jLcW_MnCfbLN8Ph-bsTwGw",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "1",    "publishTime": "2019-02-14T21:08:00Z",    "sourceDomain": "gamestar.de",    "sourceName": "GameStar",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "digital_life.games"    ],    "title": "News: Overwatch League - 2. Saison startet heute Nacht, ein einziger deutscher Spieler ist dabei",    "url": "https://www.gamestar.de/artikel/overwatch-league-2-saison-startet-heute-nacht-ein-einziger-deutscher-spieler-ist-dabei,3340648.amp"  }',  # noqa
            },
            {
                "TIMESTAMP": "2019-02-15 03:07:04.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "home_teaser_tapped",
                "MD5(USER_ID)": "d09d39006ee0b4588c4db9545bfccd5e",
                "ATTRIBUTES": '{    "category": "digital_life",    "id": "jLcW_MnCfbLN8Ph-bsTwGw",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "1",    "publishTime": "2019-02-14T21:08:00Z",    "sourceDomain": "gamestar.de",    "sourceName": "GameStar",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "digital_life.games"    ],    "title": "News: Overwatch League - 2. Saison startet heute Nacht, ein einziger deutscher Spieler ist dabei",    "url": "https://www.gamestar.de/artikel/overwatch-league-2-saison-startet-heute-nacht-ein-einziger-deutscher-spieler-ist-dabei,3340648.amp"  }',  # noqa
            },
        ]

        expected = ReportServiceResult(
            article_performance_report=ArticlePerformanceReport([]),
            user_performance_report=UserPerformanceReport([]),
        )
        received = ReportService(raw_events).create_performance_reports()
        self.assertEqual(expected, received)
