import sys
sys.path.insert(0, "../../../../../api")

from typing import Callable
from loguru import logger
from security import Credentials, JwtTokenController
from .base_handlers import BaseHandler, SecuredHandler
from versions.v0_1.message import JRPCRequest, SecuredJRPCRequest
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse
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
            return self.wrap_invalid_response("login parameter must be specified")
        if name is None:
            return self.wrap_invalid_response("name parameter must be specified")
        if surname is None:
            return self.wrap_invalid_response("surname parameter must be specified")
        if password is None:
            return self.wrap_invalid_response("password parameter must be specified")
        if email is None:
            return self.wrap_invalid_response("email parameter must be specified")

        try:
            user = self.user_interactor.create(login, password, email, name, surname)
        except ValueError as e:
            return self.wrap_invalid_response(str(e))
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
        user_json = user.json()

        return JRPCSuccessResponse(user_json, payload.id)


class AuthHandler(BaseHandler):

    def __init__(self, user_interactor: Callable, jwt_controller: JwtTokenController):
        self.user_interactor = user_interactor
        self.jwt_controller = jwt_controller

    def method(self) -> str:
        return "auth.auth"

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        email = payload.obtrain_param('email')
        password = payload.obtrain_param('password')

        if email is None:
            return self.wrap_invalid_response("email parameter must be specified")
        if password is None:
            return self.wrap_invalid_response("password parameter must be specified")

        try:
            user = self.user_interactor.auth(email, password)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        if user is None:
            return self.wrap_invalid_response("Password or email is incorrect")

        base_credentials = Credentials(user.id)
        full_credentials = self.jwt_controller.generate_full_credentials(base_credentials)


        user_json = user.json()
        credentials_json = {
            "access_token": full_credentials.access_token,
            "refresh_token": full_credentials.refresh_token
        }

        response = {
            "user": user_json,
            "credentials": credentials_json
        }

        return JRPCSuccessResponse(response, payload.id)


class RefreshCredentialsController(SecuredHandler):

    def __init__(self, jwt_controller: JwtTokenController):
        self.jwt_controller = jwt_controller

    def need_access_token(self) -> bool:
        return False

    def method(self) -> str:
        return "auth.refresh_credentials"

    def process(self, payload: SecuredJRPCRequest) -> BaseJRPCResponse:
        if not self.jwt_controller.is_refresh_token_valid(payload.credentials):
            return self.wrap_invalid_response("Refresh token is invalid or expired")

        refresh_creds = self.jwt_controller.generate_full_credentials(payload.credentials)

        response = {
            "access_token": refresh_creds.access_token,
            "refresh_token": refresh_creds.refresh_token
        }

        return JRPCSuccessResponse(response, payload.id)
