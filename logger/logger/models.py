import datetime

from sqlalchemy import (
    Column, DateTime, Integer, String, Text
)
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)


class Tweet(DeclarativeBase):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    twitter_id = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    tweet = Column(Text, nullable=False)
    retweet_count = Column(Integer)
    location = Column(String)
    place = Column(String)
