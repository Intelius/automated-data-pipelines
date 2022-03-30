# File that will store the endpoints for getting market data from our databases

from datetime import date, datetime
from fastapi import Depends, APIRouter
from typing import Optional

# import requests

import src.processedData.pydantic.newsDescription_pydantic as pydanticSchemas
import src.processedData.CRUD.newsDescription_CRUD as CRUD
from ...general.dependencies import  DBSessionManager
from ...general.exceptions import notFound_exception


router = APIRouter(prefix="/news", tags=["News Description"])

@router.get(
    "/description", response_model=list[pydanticSchemas.newsSentimentDescription]
)
def getNewsSentiment(
    #db=Depends(get_prediction_db),
    #dbDescription=Depends(get_common_db),
    ticker,
    day: Optional[date] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
):
    """
    Returns the news sentiment prediction and description.
    The search criteria options are:
    * Day: Date format: yyyy-mm-dd;
    * Ticker: Stock symbol;
    * Limit: max number of news to return;
    * Skip: number of news to skip before returning news.
    """
    with DBSessionManager() as db:

        newsSentiment = CRUD.getNewsSentiment(db, ticker, limit, skip, day)
        if newsSentiment == []:
            raise notFound_exception
        
        newsSentimentAndDescription = []

        for i in newsSentiment:
            newsSentimentDescription = CRUD.getNewsDetailBySentimentId(
                db, i.id
            )

            tickersSentimentList = []
            tickersSentiment = {}
            tickersSentiment["ticker"] = i.ticker
            tickersSentiment["compound_influence_score"] = i.compound_influence_score
            tickersSentiment["sentiment_score"] = i.sentiment_score
            tickersSentimentList.append(tickersSentiment)

            description = newsSentimentDescription.description

            if len(newsSentimentDescription.description) > 256:
                newsSentimentDescription.description = description[0:250] + "..."
            

            singleNewsSentiment = {}
            singleNewsSentiment["news_sentiment"] = tickersSentiment
            singleNewsSentiment["news_sentiment_description"] = newsSentimentDescription
            newsSentimentAndDescription.append(singleNewsSentiment)

        return newsSentimentAndDescription