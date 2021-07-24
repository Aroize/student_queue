from typing import Optional, List, Any
from ..dao import DBAccessor
from .user import User



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

    def update(self, user: User):
        with self.accessor().session() as session:
            values = {
                "id": user.id,
                "login": user.login,
                "password": user.password,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "email_confirmed": user.email_confirmed,
                "registration_timestamp": user.registration_timestamp
            }
            session.query(User).filter_by(id=user.id).update(values)
            session.commit()

    def select_all(self) -> List[User]:
        with self.accessor().session() as session:
            return session.query(User).all()

    def _find_user_by_unique_param(self, param_name: str, param_value: Any) -> Optional[User]:
        param = {param_name: param_value}
        with self.accessor().session() as session:
            return session.query(User) \
                .filter_by(**param) \
                .first()

    def find_user_by_id(self, id: int) -> Optional[User]:
        return self._find_user_by_unique_param('id', id)

    def find_user_by_email(self, email: str) -> Optional[User]:
        return self._find_user_by_unique_param('email', email)

    def find_user_by_login(self, login: str) -> Optional[User]:
        return self._find_user_by_unique_param('login', login)
