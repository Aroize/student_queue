import re
import random
from hashlib import sha256
from datetime import datetime
from .dao import DBAccessor, Base
from sqlalchemy.orm import relationship
from typing import Optional, List, Callable
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey

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


class UserEmailConfirmation(Base):
    __tablename__ = "user_confirmation"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    code = Column(Integer)

    def __str__(self):
        return """UserEmailConfirmation[id={}, code={}]""".format(self.id, self.code)


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


    def select_all(self) -> List[User]:
        with self.accessor().session() as session:
            return session.query(User).all()


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


class UserEmailConfirmationRepository:

    def __init__(self):
        self.accessor = DBAccessor

    def create(self, id: int) -> UserEmailConfirmation:
        code = random.randint(100000, 999999)
        with self.accessor().session() as session:
            session.query(UserEmailConfirmation).filter_by(id=id).delete()
            session.expire_on_commit = False

            user_confirmation = UserEmailConfirmation(id=id, code=code)
            session.add(user_confirmation)
            session.flush()
            session.commit()
            return user_confirmation

    def select_all(self) -> List[UserEmailConfirmation]:
        with self.accessor().session() as session:
            return session.query(UserEmailConfirmation).all()



# INTERACTOR

class UserInteractor:

    def __init__(
        self,
        user_repository: UserRepository,
        email_confirmation: UserEmailConfirmationRepository,
        mail_service: Callable
        ):

        self.user_repository = user_repository
        self.email_confirmation_repository = email_confirmation
        self.mail_service = mail_service

        login_regex = r"[A-Za-z0-9_]{4,15}"
        self.login_regex = re.compile(login_regex)
        email_regex = r"(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        self.email_regex = re.compile(email_regex)
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[_a-zA-Z\d]{8,15}$"
        self.password_regex = re.compile(password_regex)


    def create(
        self,
        login: str,
        password: str,
        email: str,
        name: str,
        surname: str
        ) -> User:
        name = name.strip()
        surname = surname.strip()

        if len(name) not in range(2, 20):
            raise ValueError("Name length must be in range [2, 20)")

        if len(surname) not in range(2, 40):
            raise ValueError("Surname length must be in range[2, 40)")

        if not self.login_regex.match(login):
            raise ValueError("Login length must be greater than 3, less than 16, no special characters allowed")

        if not self.password_regex.match(password):
            raise ValueError("Password must be minimum 8 and maximum 16 characters and contains at least one uppercase letter, one lowercase letter and one number")

        if not self.email_regex.match(email):
            raise ValueError("Email format isn't supported")

        password_hash = sha256(password.encode()).hexdigest()

        user = self.user_repository.create(login, password_hash, email, name, surname)
        confirmation = self.email_confirmation_repository.create(user.id)
        url = self.build_verification_url(confirmation.code)
        self.mail_service.send_verification_email(url)

        return user


    def list(self) -> List[String]:
        """Returns list of all users with data"""
        users = self.user_repository.select_all()
        return list(map(str, users))


    # TODO(): remove this hardcode, mode to some controller
    def build_verification_url(self, code):
        return "http://localhost:5022/verify_email?code={}".format(code)
