import abc
import codecs
import csv
import pathlib
from typing import Dict, List

import boto3
from botocore import UNSIGNED
from botocore.config import Config


class BaseDataSourceParser(abc.ABC):
    @abc.abstractmethod
    def get_raw_events(self) -> List[Dict]:
        pass


class LocalFileDataSourceParser(BaseDataSourceParser):
    def __init__(self, datasets_dir: pathlib.Path):
        self.datasets_dir = datasets_dir

    def get_raw_events(self) -> List[Dict]:
        raw_events = []
        for file_path in self.datasets_dir.iterdir():
            with open(str(file_path.absolute()), "rt", encoding="utf-8-sig") as f:
                for raw_event in csv.DictReader(f, delimiter="\t"):
                    raw_events.append(raw_event)
        return raw_events


class S3DataSourceParser(BaseDataSourceParser):
    def __init__(
        self, s3_bucket: str = "upday-data-assignment", prefix: str = "lake/"
    ) -> None:
        self.s3_bucket = boto3.resource(
            "s3", config=Config(signature_version=UNSIGNED)
        ).Bucket(s3_bucket)
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
            for row in csv.DictReader(
                codecs.getreader("utf-8-sig")(obj.get()["Body"]), delimiter="\t"
            )
        ]

    def get_raw_events(self) -> List[Dict]:
        objects = self._get_objects()
        raw_events = [
            raw_event for obj in objects for raw_event in self._get_object_data(obj)
        ]
        return raw_events
