import re
from hashlib import sha256
from typing import Callable
from .base_handlers import BaseHandler
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse, JRPCRequest
from versions.v0_1.exceptions import JRPCErrorCode


class RegistrationHandler(BaseHandler):

    def __init__(self, user_repository: Callable):
        self.user_repository = user_repository
        login_regex = r"[A-Za-z0-9_]{4,15}"
        self.login_regex = re.compile(login_regex)
        email_regex = r"(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        self.email_regex = re.compile(email_regex)
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[_a-zA-Z\d]{8,15}$"
        self.password_regex = re.compile(password_regex)


    def method(self) -> str:
        return "auth.register"


    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        login = payload.obtrain_param('login')
        name = payload.obtrain_param('name')
        surname = payload.obtrain_param('surname')
        password = payload.obtrain_param('password')
        email = payload.obtrain_param('email')

        if login is None:
            return self.__wrap_invalid__("login parameter must be specified")
        if name is None:
            return self.__wrap_invalid__("name parameter must be specified")
        if surname is None:
            return self.__wrap_invalid__("surname parameter must be specified")
        if password is None:
            return self.__wrap_invalid__("password parameter must be specified")
        if email is None:
            return self.__wrap_invalid__("email parameter must be specified")

        name = name.strip()
        surname = surname.strip()

        if len(name) not in range(2, 20):
            return self.__wrap_invalid__("Name length must be in range [2, 20)")

        if len(surname) not in range(2, 40):
            return self.__wrap_invalid__("Surname length must be in range[2, 40)")

        if not self.login_regex.match(login):
            return self.__wrap_invalid__("Login length must be greater than 3, less than 16, no special characters allowed")

        if not self.password_regex.match(password):
            return self.__wrap_invalid__("Password must be minimum 8 and maximum 16 characters and contains at least one uppercase letter, one lowercase letter and one number")

        if not self.email_regex.match(email):
            return self.__wrap_invalid__("Email format isn't supported")

        password_hash = sha256(password.encode()).hexdigest()

        try:
            user = self.user_repository.create(login, password_hash, email, name, surname)
        except RuntimeError as e:
            msg = str(e)
            return JRPCErrorResponse(
                JRPCErrorCode.EntityAlreadyExists.value,
                msg,
                payload.id
            )
        except Exception:
            return JRPCErrorResponse(
                JRPCErrorCode.InternalError.value,
                "Exception thrown during inserting into database",
                payload.id
            )

        # user must be specified
        user_json = {
            "id": user.id,
            "login": user.login,
            "email": user.email,
            "name": user.name,
            "surname": user.surname
        }

        return JRPCSuccessResponse(user_json, payload.id)


    def __wrap_invalid__(self, message: str) -> JRPCErrorResponse:
        return JRPCErrorResponse(
            JRPCErrorCode.InvalidParameters.value,
            message,
            None
        )
