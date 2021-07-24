from datetime import datetime
from ..dao import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    email_confirmed = Column(Boolean, default=False)
    registration_timestamp = Column(DateTime, default=datetime.utcnow)

    def json(self) -> dict:
        return {
            "id": self.id,
            "login": self.login,
            "email": self.email,
            "name": self.name,
            "surname": self.surname
        }

    def __repr__(self):
        return f'User[id = {self.id}, ' \
               f'login = {self.login}, ' \
               f'password = {self.password}, ' \
               f'email = {self.email}, ' \
               f'name = {self.name}, ' \
               f'surname = {self.surname}, ' \
               f'email_confirmed = {self.email_confirmed}, ' \
               f'timestamp = {self.registration_timestamp}]'
