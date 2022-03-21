import datetime
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class EventType(str, Enum):
    TOP_NEWS_CARD_VIEWED = "top_news_card_viewed"
    MY_NEWS_CARD_VIEWED = "my_news_card_viewed"
    ARTICLE_VIEWED = "article_viewed"


@dataclass
class ArticleEvent:
    article_id: str
    user_id: str
    event_type: EventType
    date: datetime.date
    article_title: str
    article_category: str


@dataclass
class Stats:
    card_views: int = 0
    article_views: int = 0

    def __iadd__(self, other):
        self.card_views += other.card_views
        self.article_views += other.article_views
        return self


@dataclass
class UserArticleDailyStats:
    article_id: str
    user_id: str
    date: datetime.date
    card_views: int = 0
    article_views: int = 0


@dataclass(frozen=True)
class UserPerformanceRow:
    user_id: str
    date: datetime.date
    ctr: Optional[float] = 0.0


@dataclass(frozen=True)
class ArticlePerformanceRow:
    article_id: str
    date: datetime.date
    article_title: str
    article_category: str
    card_views: int = 0
    article_views: int = 0


@dataclass
class UserPerformanceReport:
    data: List[UserPerformanceRow]


@dataclass
class ArticlePerformanceReport:
    data: List[ArticlePerformanceRow]


@dataclass
class Article:
    title: str
    category: str


@dataclass(frozen=True)
class ArticlePerformancePK:
    article_id: str
    date: datetime.date

    @classmethod
    def from_event(cls, event: ArticleEvent):
        return cls(
            article_id=event.article_id,
            date=event.date,
        )


@dataclass(frozen=True)
class UserPerformancePK:
    user_id: str
    date: datetime.date

    @classmethod
    def from_event(cls, event: ArticleEvent):
        return cls(
            user_id=event.user_id,
            date=event.date,
        )


@dataclass
class ReportServiceResult:
    article_performance_report: ArticlePerformanceReport
    user_performance_report: UserPerformanceReport
