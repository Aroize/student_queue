import re
import random
from hashlib import sha256
from typing import Optional
import inject
from .user import User
from .user_repository import UserRepository
from .user_email_confirmation_repository import UserEmailConfirmationRepository
from backend.api.mail_service import MailSenderService


class UserInteractor:
    def __init__(self):
        login_regex = r"[A-Za-z0-9_]{4,15}"
        self.login_regex = re.compile(login_regex)
        email_regex = r"(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c" \
                      r"\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9]" \
                      r"(?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|" \
                      r"1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*" \
                      r"[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        self.email_regex = re.compile(email_regex)
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[_a-zA-Z\d]{8,15}$"
        self.password_regex = re.compile(password_regex)

    @inject.params(mail_service=MailSenderService,
                   user_repository=UserRepository,
                   email_confirmation_repository=UserEmailConfirmationRepository)
    def create(
        self,
        login: str,
        password: str,
        email: str,
        name: str,
        surname: str,
        mail_service: MailSenderService = None,
        user_repository: UserRepository = None,
        email_confirmation_repository: UserEmailConfirmationRepository = None
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
            raise ValueError("Password must be minimum 8 and maximum 16 characters and contains at "
                             "least one uppercase letter, one lowercase letter and one number")

        if not self.email_regex.match(email):
            raise ValueError("Email format isn't supported")

        password_hash = sha256(password.encode()).hexdigest()

        user = user_repository.create(login, password_hash, email, name, surname)
        code = random.randint(100000, 999999)
        confirmation = email_confirmation_repository.create(user.id, code)
        url = self.build_verification_url(confirmation.id, confirmation.code)
        mail_service.send_verification_email(url)

        return user

    @inject.params(user_repository=UserRepository,
                   email_confirmation_repository=UserEmailConfirmationRepository)
    def confirm_email(self,
                      id: int,
                      code: int,
                      user_repository: UserRepository = None,
                      email_confirmation_repository: UserEmailConfirmationRepository = None) -> bool:

        confirmation = email_confirmation_repository.find_confirmation_by_user(id)
        if confirmation is None or confirmation.code != code:
            return False
        email_confirmation_repository.delete_confirmation_by_user(id)

        user = user_repository.find_user_by_id(id)
        user.email_confirmed = True
        user_repository.update(user)

        return True

    @inject.params(email_confirmation_repository=UserEmailConfirmationRepository)
    def fake_confirm_email(self, id: int, email_confirmation_repository: UserEmailConfirmationRepository = None) -> bool:
        confirmation = email_confirmation_repository.find_confirmation_by_user(id)
        if confirmation is None:
            return False
        confirm_code = confirmation.code
        return self.confirm_email(id, confirm_code)

    @inject.params(user_repository=UserRepository)
    def auth(self, login_email: str, raw_password: str, user_repository: UserRepository = None) -> Optional[User]:
        password = sha256(raw_password.encode()).hexdigest()
        user = user_repository.find_user_by_email(login_email) or \
               user_repository.find_user_by_login(login_email)

        if user is None:
            raise RuntimeError("No such user")
        if not user.email_confirmed:
            raise RuntimeError("Before authorization you must confirm your email")
        if user.password != password:
            raise ValueError("Password is incorrect")

        return user

    # TODO(): remove this hardcode, mode to some controller
    @staticmethod
    def build_verification_url(id: int, code: int) -> str:
        return "http://localhost:5022/verify_email?id={}&code={}".format(id, code)
