from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class DBAccessor:
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)
    first_name = Column(String)
    second_name = Column(String)
    third_name = Column(String)
    isu_number = Column(Integer) # should be in each university, idk
    registration_timestamp = Column(Integer)
