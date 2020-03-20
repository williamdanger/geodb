import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(os.getenv('GEODB_URL'), echo=True)
dbSession = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = dbSession.query_property()
