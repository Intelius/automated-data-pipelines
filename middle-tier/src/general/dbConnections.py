from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.pool import NullPool

# File that includes all of the database connections


# Class that includes the engine and session maker for the application DB
class dair_boosterpackDB:
    dbString = os.environ["automated_data_pipelines_mysql_engine"]
    engine = create_engine(
        dbString,
        pool_pre_ping=True,
        echo_pool=True,
        echo=True,
        poolclass=NullPool
        #pool_size=20,
        #max_overflow=30
    )
    dbSession = sessionmaker(autocommit=False, bind=engine, expire_on_commit=False)

# Declaring the database ORM classes
Base = declarative_base()