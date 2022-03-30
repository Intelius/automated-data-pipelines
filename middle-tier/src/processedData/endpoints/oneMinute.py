# File that will store the endpoints for getting market data from our databases

from datetime import date, datetime
from fastapi import Depends, APIRouter
from typing import Optional

# import requests

import src.processedData.pydantic.oneMinute_pydantic as pydanticSchemas
import src.processedData.CRUD.oneMinute_CRUD as CRUD
from ...general.dependencies import DBSessionManager
from ...general.exceptions import notFound_exception


router = APIRouter(prefix="/marketData", tags=["Market Data"])

@router.get("/oneMinute", response_model=list[pydanticSchemas.oneMinute])
def getOneMinData(
    ticker,
    date: Optional[date] = None,
):
    """
    Return the one minute market data for the given date and selected stock. If no date is given return
    the market data for the current day.

    Dates should be given in the form yyyy-mm-dd
    """
    with DBSessionManager() as db:
        oneMinuteData = CRUD.getOneMinData(db, ticker, date)
        if oneMinuteData == []:
            raise notFound_exception
        return oneMinuteData