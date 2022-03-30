# File that includes all of the general dependencies that will be needed by other endpoints

from .dbConnections import (
#  dair_boosterpack,
 dair_boosterpackDB
)
from datetime import datetime
from pytz import timezone
from sqlalchemy import exc
from contextlib import contextmanager

@contextmanager
def DBSessionManager():
    db = dair_boosterpackDB.dbSession()
    try:
        yield db
    except Exception as e:
        db.rollback()
        print(e)
        raise e
    finally:
        db.close()