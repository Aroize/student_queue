from typing import Callable
from .base_handlers import BaseHandler
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse, JRPCRequest
from versions.v0_1.exceptions import JRPCErrorCode


class RegistrationHandler(BaseHandler):

    def __init__(self, user_interactor: Callable):
        self.user_interactor = user_interactor


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

        try:
            user = self.user_interactor.create(login, password, email, name, surname)
        except ValueError as e:
            return self.__wrap_invalid__(str(e))
        except RuntimeError as e:
            msg = str(e)
            return JRPCErrorResponse(
                JRPCErrorCode.EntityAlreadyExists.value,
                msg,
                payload.id
            )
        except Exception as e:
            print(e)
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
