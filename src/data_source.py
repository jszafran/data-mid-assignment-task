import codecs
import csv
import datetime
import json
from typing import Dict, List

import boto3
from botocore import UNSIGNED
from botocore.config import Config

from src.types import ArticleEvent, EventType

S3_RESOURCE = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
CODEC_READER = codecs.getreader("utf-8-sig")
RELEVANT_EVENTS = (
    EventType.MY_NEWS_CARD_VIEWED,
    EventType.TOP_NEWS_CARD_VIEWED,
    EventType.ARTICLE_VIEWED,
)


class DataSourceParser:
    def __init__(
        self, s3_bucket: str = "upday-data-assignment", prefix: str = "lake/"
    ) -> None:
        self.s3_bucket = S3_RESOURCE.Bucket(s3_bucket)
        self.prefix = prefix

    def _get_objects(self):
        return [
            obj
            for obj in self.s3_bucket.objects.filter(Prefix=self.prefix)
            if obj.size > 0
        ]

    def _get_object_data(self, obj) -> List[Dict]:
        return [
            row
            for row in csv.DictReader(CODEC_READER(obj.get()["Body"]), delimiter="\t")
        ]

    def _parse_raw_event(self, raw_event) -> ArticleEvent:
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

    def read_raw_events(self) -> List[Dict]:
        objects = self._get_objects()
        raw_events = [
            raw_event for obj in objects for raw_event in self._get_object_data(obj)
        ]
        return raw_events
