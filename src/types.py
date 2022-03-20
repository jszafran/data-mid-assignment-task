import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    TOP_NEWS_CARD_VIEWED = "top_news_card_viewed"
    MY_NEWS_CARD_VIEWED = "my_news_card_viewed"
    ARTICLE_VIEWED = "article_viewed"


@dataclass
class ArticleEvent:
    article_id: str
    user_id: str
    event: EventType
    date: datetime.date
    title: str
    category: str


@dataclass
class ArticlePerformanceOutput:
    article_id: str
    user_id: str
    date: datetime.date
    title: str
    category: str
    card_views: int = 0
    article_views: int = 0


@dataclass
class UserArticleStats:
    article_id: str
    user_id: str
    date: datetime.date
    card_views: int = 0
    article_views: int = 0


@dataclass
class UserPerformanceOutput:
    user_id: str
    date: datetime.date
    ctr: Optional[float] = 0.0


@dataclass
class UserPerformanceStats:
    user_id: str
    date: datetime.date
    article_views: int = 0
    card_views: int = 0

    def get_user_performance(self) -> UserPerformanceOutput:
        # TODO: do sanity check if self.card_views != 0
        return UserPerformanceOutput(
            user_id=self.user_id,
            date=self.date,
            ctr=round(self.article_views / self.card_views, 2),
        )
