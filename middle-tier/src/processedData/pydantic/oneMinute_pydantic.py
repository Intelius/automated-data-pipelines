# File for all of the pydantic models that will be used for the one minute market data endpoint
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Object that is used when sending one minute market data back to the user
class oneMinute(BaseModel):
    ticker: Optional[str]
    high: Optional[float]
    low: Optional[float]
    open: Optional[float]
    close: Optional[float] 
    volume: Optional[float]
    datetime: Optional[datetime]
    EMA9: Optional[float]

    # Config orm-mode is needed to prevent lazy loading from sqlalchemy and
    #   ensure all data is present when sending data back to user
    class Config:
        orm_mode = True