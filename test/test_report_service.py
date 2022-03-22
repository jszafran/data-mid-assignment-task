import datetime
from unittest import TestCase

from src.report_service import ReportService
from src.types import (
    ArticlePerformance,
    ArticlePerformanceReport,
    ReportServiceResult,
    UserPerformance,
    UserPerformanceReport,
)


# TODO: split tests for article performance & user performance reports into separate test functions
class TestReportService(TestCase):
    def test_if_report_generated_from_valid_events_has_correct_values(self):
        raw_events = [
            {
                "TIMESTAMP": "2019-02-15 03:07:03.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "my_news_card_viewed",
                "MD5(USER_ID)": "user1",
                "ATTRIBUTES": '{    "category": "Cat1",    "id": "art1",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "1",    "publishTime": "2019-02-14T21:08:00Z",    "sourceDomain": "gamestar.de",    "sourceName": "GameStar",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "digital_life.games"    ],    "title": "Title1",    "url": "https://www.gamestar.de/artikel/overwatch-league-2-saison-startet-heute-nacht-ein-einziger-deutscher-spieler-ist-dabei,3340648.amp"  }',  # noqa
            },
            {
                "TIMESTAMP": "2019-02-15 03:07:04.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "article_viewed",
                "MD5(USER_ID)": "user1",
                "ATTRIBUTES": '{    "category": "Cat1",    "id": "art1",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "1",    "publishTime": "2019-02-14T21:08:00Z",    "sourceDomain": "gamestar.de",    "sourceName": "GameStar",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "digital_life.games"    ],    "title": "Title1",    "url": "https://www.gamestar.de/artikel/overwatch-league-2-saison-startet-heute-nacht-ein-einziger-deutscher-spieler-ist-dabei,3340648.amp"  }',  # noqa
            },
            {
                "TIMESTAMP": "2019-02-15 03:07:38.231 +0000",
                "MD(SESSION_ID)": "96eafb749b446580ae38e678777c734a",
                "EVENT_NAME": "top_news_card_viewed",
                "MD5(USER_ID)": "user2",
                "ATTRIBUTES": '{    "category": "Cat2",    "id": "art2",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "235",    "publishTime": "2019-02-14T20:53:00Z",    "sourceDomain": "maisfutebol.iol.pt",    "sourceName": "Maisfutebol",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "sports.football_domestic"    ],    "title": "Title2",    "url": "https://maisfutebol.iol.pt/amp/liga/fabio-coentrao/rio-ave-coentrao-regressa-aos-convocados-para-o-santa-clara"  }',  # noqa
            },
            {
                "TIMESTAMP": "2019-02-15 03:10:38.231 +0000",
                "MD(SESSION_ID)": "f2a48d248a0152f4091ad1dd0186586b",
                "EVENT_NAME": "my_news_card_viewed",
                "MD5(USER_ID)": "user3",
                "ATTRIBUTES": '{    "category": "Cat2",    "id": "art2",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "235",    "publishTime": "2019-02-14T20:53:00Z",    "sourceDomain": "maisfutebol.iol.pt",    "sourceName": "Maisfutebol",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "sports.football_domestic"    ],    "title": "Title2",    "url": "https://maisfutebol.iol.pt/amp/liga/fabio-coentrao/rio-ave-coentrao-regressa-aos-convocados-para-o-santa-clara"  }',  # noqa
            },
            {
                "TIMESTAMP": "2019-02-17 03:10:38.231 +0000",
                "MD(SESSION_ID)": "f2a48d248a0152f4091ad1dd0186586b",
                "EVENT_NAME": "article_viewed",
                "MD5(USER_ID)": "user3",
                "ATTRIBUTES": '{    "category": "Cat2",    "id": "art2",    "noteType": "TRENDING_SOCIAL",    "orientation": "PORTRAIT",    "position": "235",    "publishTime": "2019-02-14T20:53:00Z",    "sourceDomain": "maisfutebol.iol.pt",    "sourceName": "Maisfutebol",    "stream": "wtk",    "streamType": "my news",    "subcategories": [      "sports.football_domestic"    ],    "title": "Title2",    "url": "https://maisfutebol.iol.pt/amp/liga/fabio-coentrao/rio-ave-coentrao-regressa-aos-convocados-para-o-santa-clara"  }',  # noqa
            },
        ]

        reports = ReportService(raw_events).create_performance_reports()

        # test article performance data
        expected_article_performance_rows = {
            ArticlePerformance(
                "art1", datetime.date(2019, 2, 15), "Title1", "Cat1", 1, 1
            ),
            ArticlePerformance(
                "art2", datetime.date(2019, 2, 15), "Title2", "Cat2", 2, 0
            ),
            ArticlePerformance(
                "art2", datetime.date(2019, 2, 17), "Title2", "Cat2", 0, 1
            ),
        }

        self.assertEqual(
            expected_article_performance_rows,
            set(reports.article_performance_report.data),
        )

        # test user performance data
        expected_user_performance_rows = {
            UserPerformance("user1", datetime.date(2019, 2, 15), 1.0),
            UserPerformance("user2", datetime.date(2019, 2, 15), 0.0),
            UserPerformance("user3", datetime.date(2019, 2, 15), 0.0),
            UserPerformance("user3", datetime.date(2019, 2, 17), None),
        }

        self.assertEqual(
            expected_user_performance_rows,
            set(reports.user_performance_report.data),
        )

    def test_if_irrelevant_events_are_skipped(self):
        raw_events = [
            {
                "TIMESTAMP": "2019-02-15 03:07:03.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "content_shared",
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
            {
                "TIMESTAMP": "2019-02-15 03:07:04.662 +0000",
                "MD5(SESSION_ID)": "60584c4ed725b4554397e3a99ecf79bb",
                "EVENT_NAME": "bottom_navigation_bar_clicked",
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
