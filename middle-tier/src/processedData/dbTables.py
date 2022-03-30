# File for the database table ORM classes used in processed data

from ..general.dbConnections import (
    Base,
    dair_boosterpackDB
)
from sqlalchemy import *

# --------------------------------------------------------------------------
# ORM classes for processed data

# ORM class for one minute data stored in marketdata_1minute generated from database schema
class onemindata(Base):
    __table__ = Table(
        "marketdata_1minute",
        Base.metadata,
        autoload=True,
        autoload_with=dair_boosterpackDB.engine,
        schema="dair_boosterpack",
    )


# ORM class for news description data stored in news_drescription generated from database schema
class news_description(Base):
    __table__ = Table(
        "news_description",
        Base.metadata,
        autoload=True,
        autoload_with=dair_boosterpackDB.engine,
        schema="dair_boosterpack",
    )

# ORM class for news sentiments data stored in news_sentiment_prediction generated from database schema
class news_sentiment_prediction(Base):
    __table__ = Table(
        "news_sentiment_prediction",
        Base.metadata,
        autoload=True,
        autoload_with=dair_boosterpackDB.engine,
        schema="dair_boosterpack",
    )