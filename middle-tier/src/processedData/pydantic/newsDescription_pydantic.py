# File for all of the pydantic models that will be used for the news description endpoint
from pydantic import BaseModel, PositiveInt
from datetime import datetime, date
from typing import Optional

from pydantic.errors import FloatError

# Object that is used when sending news description data back to the user
class news_description(BaseModel):
    id: str
    title:str
    author: str
    article_url: str
    description: str
    publisher: str
    tickers: str
    keywords: str
    datetime: datetime
    image_url: Optional[str]

    # Config orm-mode is needed to prevent lazy loading from sqlalchemy and
    #   ensure all data is present when sending data back to user
    class Config:
        orm_mode = True

# Object that is used when sending news sentiment data back to the user
class news_sentiment(BaseModel):
    ticker: str
    compound_influence_score: float
    sentiment_score: str

    # Config orm-mode is needed to prevent lazy loading from sqlalchemy and
    #   ensure all data is present when sending data back to user
    class Config:
        orm_mode = True

class newsSentimentDescription(BaseModel):
    news_sentiment: news_sentiment
    news_sentiment_description: news_description

    # Config orm-mode is needed to prevent lazy loading from sqlalchemy and
    #   ensure all data is present when sending data back to user
    class Config:
        orm_mode = True
