from typing import Optional
from datetime import datetime
from .dao import DBAccessor, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, DateTime, Boolean

# TABLE

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


    def __str__(self):
        return """User[id = {}, login = {}, password = {}, email = {}, name = {}, surname = {}, email_confirmed = {}, timestamp = {}]""".format(
            self.id,
            self.login,
            self.password,
            self.email,
            self.name,
            self.surname,
            self.email_confirmed,
            self.registration_timestamp
        )


# REPOSITORY

class UserRepository:

    def __init__(self):
        self.accessor = DBAccessor

    def create(
        self,
        login: str,
        password: str,
        email: str,
        name: str,
        surname: str
        ) -> User:
        with self.accessor().session() as session:
            if session.query(User).filter_by(email=email).count() > 0:
                raise RuntimeError("User with this email already exists")
            if session.query(User).filter_by(login=login).count() > 0:
                raise RuntimeError("User with this login already exists")
            session.expire_on_commit = False
            user = User(
                login=login,
                password=password,
                email=email,
                name=name,
                surname=surname
            )
            session.add(user)
            session.flush()
            session.commit()
            return user


    def insert(self, user: User):
        with self.accessor().session() as session:
            session.add(user)
            session.commit()


    def find_user_by_id(self, id: int) -> Optional[User]:
        with self.accessor().session() as session:
            return session.query(User) \
                .filter_by(id=id) \
                .first()


    def find_user_by_email(self, email: str) -> Optional[User]:
        with self.accessor().session() as session:
            return session.query(User) \
                .filter_by(email=email) \
                .first()
