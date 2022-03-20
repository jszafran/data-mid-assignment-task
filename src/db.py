from typing import Union

from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import mapper, sessionmaker

from src.types import (
    ArticlePerformanceReport,
    ArticlePerformanceRow,
    UserPerformanceReport,
    UserPerformanceRow,
)

metadata = MetaData()
article_performance_table = Table(
    "article_performance",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("article_id", String(100)),
    Column("date", Date),
    Column("article_title", String(600)),
    Column("article_category", String(100)),
    Column("card_views", Integer, nullable=True),
    Column("article_views", Integer, nullable=True),
    UniqueConstraint("article_id", "date", name="uix_article_id_date"),
)

user_performance_table = Table(
    "user_performance",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String(100)),
    Column("date", Date),
    Column("ctr", Float),
    UniqueConstraint("user_id", "date", name="uix_user_id_date"),
)

mapper(ArticlePerformanceRow, article_performance_table)
mapper(UserPerformanceRow, user_performance_table)


class DBManager:
    def __init__(self, conn_str: str):
        engine = create_engine(conn_str)
        self.session = sessionmaker(bind=engine)()
        metadata.drop_all(engine)
        metadata.create_all(engine)

    def load_report(
        self, report: Union[UserPerformanceReport, ArticlePerformanceReport]
    ) -> None:
        # TODO: bulk insert in case of data would be bigger?
        for row in report.data:
            self.session.add(row)
        self.session.commit()
