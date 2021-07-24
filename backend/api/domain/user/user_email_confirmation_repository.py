from ..dao import DBAccessor
from typing import Optional, List
from .user_email_confirmation import UserEmailConfirmation


class UserEmailConfirmationRepository:

    def __init__(self):
        self.accessor = DBAccessor

    def create(self, id: int, code: int) -> UserEmailConfirmation:
        with self.accessor().session() as session:
            session.query(UserEmailConfirmation).filter_by(id=id).delete()

            user_confirmation = UserEmailConfirmation(id=id, code=code)
            session.add(user_confirmation)
            session.flush()
            session.commit()
            return user_confirmation

    def find_confirmation_by_user(self, id: int) -> Optional[UserEmailConfirmation]:
        with self.accessor().session() as session:
            return session.query(UserEmailConfirmation) \
                .filter_by(id=id) \
                .first()

    def delete_confirmation_by_user(self, id: int):
        with self.accessor().session() as session:
            session.query(UserEmailConfirmation) \
                .filter_by(id=id) \
                .delete()
            session.commit()

    def select_all(self) -> List[UserEmailConfirmation]:
        with self.accessor().session() as session:
            return session.query(UserEmailConfirmation).all()
