# File that includes all of the database interactions (Create, Read, Update, Delete)
# that will be used for one minute market data

from sqlalchemy.sql.expression import cast
import src.processedData.dbTables as dbTables
from sqlalchemy.orm import Session
from sqlalchemy import Date
from datetime import date


def getOneMinData(db: Session, ticker:str, day: str):
    if not day:
        day = date.today()
    return (
        db.query(dbTables.onemindata)
        .filter(cast(dbTables.onemindata.datetime, Date) == day, dbTables.onemindata.ticker == ticker)
        .order_by(dbTables.onemindata.datetime)
        .all()
    )