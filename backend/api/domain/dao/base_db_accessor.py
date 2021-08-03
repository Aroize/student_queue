from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseDBAccessor:
    def __init__(self):
        # Creates db connector
        raise NotImplemented

    def session(self) -> Session:
        raise NotImplemented
