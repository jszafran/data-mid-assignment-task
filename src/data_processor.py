import datetime
import json
from typing import Dict, List

from src.types import ArticleEvent, EventType

RELEVANT_EVENTS = (
    EventType.ARTICLE_VIEWED,
    EventType.TOP_NEWS_CARD_VIEWED,
    EventType.MY_NEWS_CARD_VIEWED,
)


class EventProcessor:
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
            event=raw_event.get("EVENT_NAME"),
            date=datetime.datetime.strptime(
                raw_event.get("TIMESTAMP")[:10], "%Y-%m-%d"
            ).date(),
            title=attributes.get("title"),
            category=attributes.get("category"),
        )

    def _parse_raw_events(self, raw_events) -> List[ArticleEvent]:
        return [self._parse_event(raw_event) for raw_event in raw_events]
