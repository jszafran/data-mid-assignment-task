import datetime
import json
from collections import defaultdict
from typing import Dict, List

from src.types import (
    Article,
    ArticleEvent,
    ArticlePerformancePK,
    ArticlePerformanceReport,
    ArticlePerformanceRow,
    EventType,
    ReportServiceResult,
    Stats,
    UserPerformancePK,
    UserPerformanceReport,
    UserPerformanceRow,
)

RELEVANT_EVENTS = (
    EventType.ARTICLE_VIEWED,
    EventType.TOP_NEWS_CARD_VIEWED,
    EventType.MY_NEWS_CARD_VIEWED,
)


class ReportService:
    def __init__(self, raw_events: List[Dict]) -> None:
        self._raw_events = raw_events

    def _filter_relevant_events(self) -> List[Dict]:
        return [
            event
            for event in self._raw_events
            if event.get("EVENT_NAME") in RELEVANT_EVENTS
        ]

    def _parse_event(self, raw_event: Dict) -> ArticleEvent:
        attributes = json.loads(raw_event.get("ATTRIBUTES"))

        return ArticleEvent(
            article_id=attributes.get("id"),
            user_id=raw_event.get("MD5(USER_ID)"),
            event_type=raw_event.get("EVENT_NAME"),
            date=datetime.datetime.strptime(
                raw_event.get("TIMESTAMP")[:10], "%Y-%m-%d"
            ).date(),
            article_title=attributes.get("title"),
            article_category=attributes.get("category"),
        )

    def _parse_raw_events(self, raw_events: List[Dict]) -> List[ArticleEvent]:
        return [self._parse_event(raw_event) for raw_event in raw_events]

    def _create_user_performance_report(
        self,
        user_performance_stats: Dict[UserPerformancePK, Stats],
    ) -> UserPerformanceReport:
        user_performance_data = []
        for pk, stats in user_performance_stats.items():
            try:
                ctr = round(stats.article_views / stats.card_views, 2)
            except ZeroDivisionError:
                ctr = None

            user_performance_data.append(
                UserPerformanceRow(
                    user_id=pk.user_id,
                    date=pk.date,
                    ctr=ctr,
                )
            )

        return UserPerformanceReport(user_performance_data)

    def _create_article_performance_report(
        self,
        article_performance_stats: Dict[ArticlePerformancePK, Stats],
        articles: Dict[str, Article],
    ) -> ArticlePerformanceReport:
        article_performance_report_data = []
        for pk, stats in article_performance_stats.items():
            article = articles.get(pk.article_id)
            article_performance_report_data.append(
                ArticlePerformanceRow(
                    article_id=pk.article_id,
                    date=pk.date,
                    article_title=article.title,
                    article_category=article.category,
                    card_views=stats.card_views,
                    article_views=stats.article_views,
                )
            )

        return ArticlePerformanceReport(article_performance_report_data)

    def create_performance_reports(self) -> ReportServiceResult:
        articles = {}
        article_performance_stats = defaultdict(Stats)
        user_performance_stats = defaultdict(Stats)
        filtered_events = self._filter_relevant_events()
        parsed_events = self._parse_raw_events(filtered_events)

        for event in parsed_events:
            card_views = (
                1
                if event.event_type
                in (EventType.MY_NEWS_CARD_VIEWED, EventType.TOP_NEWS_CARD_VIEWED)
                else 0
            )
            article_views = 1 if event.event_type == EventType.ARTICLE_VIEWED else 0

            stats = Stats(card_views=card_views, article_views=article_views)
            # group by article_id, date
            article_performance_stats[ArticlePerformancePK.from_event(event)] += stats
            # group by user_id, date
            user_performance_stats[UserPerformancePK.from_event(event)] += stats

            if event.article_id not in articles:
                articles[event.article_id] = Article(
                    title=event.article_title, category=event.article_category
                )

        article_performance_report = self._create_article_performance_report(
            article_performance_stats,
            articles,
        )
        user_performance_report = self._create_user_performance_report(
            user_performance_stats
        )

        return ReportServiceResult(
            article_performance_report=article_performance_report,
            user_performance_report=user_performance_report,
        )
