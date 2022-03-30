# File that includes all of the database interactions (Create, Read, Update, Delete)
# that will be used for News Description

from pydantic.types import StrBytes
from sqlalchemy.sql.elements import or_
from sqlalchemy.sql.expression import cast
import src.processedData.dbTables as dbTables
from sqlalchemy.orm import Session
from sqlalchemy import Date
from datetime import date, datetime, timedelta
from pytz import timezone
from sqlalchemy.sql import func, tuple_


def getNewsSentiment(
    db: Session, ticker: str, limit: int, skip: int, day:str
):
    if not day:
            day = date.today()
    return (
        db.query(dbTables.news_sentiment_prediction.id,dbTables.news_sentiment_prediction.ticker,dbTables.news_sentiment_prediction.compound_influence_score, dbTables.news_sentiment_prediction.sentiment_score )
        .filter(
            dbTables.news_sentiment_prediction.ticker == ticker,
            # cast(dbTables.news_sentiment_prediction.datetime, Date) == day
            (dbTables.news_sentiment_prediction.datetime)
            > (day - timedelta(days=3)),
            cast(dbTables.news_sentiment_prediction.datetime, Date) <= day
        )
        .group_by(dbTables.news_sentiment_prediction.id,dbTables.news_sentiment_prediction.ticker,dbTables.news_sentiment_prediction.datetime,dbTables.news_sentiment_prediction.compound_influence_score, dbTables.news_sentiment_prediction.sentiment_score )
        .order_by((dbTables.news_sentiment_prediction.datetime.desc()))
        .offset(skip)
        .limit(limit)
        .all()
    )


def getNewsDetailBySentimentId(db: Session, sentiment_id: str):

    return (
        db.query(dbTables.news_description)
        .filter((dbTables.news_description.id == sentiment_id))
        .first()
    )

