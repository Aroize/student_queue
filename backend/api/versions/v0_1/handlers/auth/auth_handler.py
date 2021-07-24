from typing import Callable
from ..base import BaseHandler
from backend.api.jrpc import BaseJRPCResponse, JRPCRequest, JRPCSuccessResponse
from backend.api.security import JwtTokenController, Credentials



class AuthHandler(BaseHandler):

    def __init__(self, user_interactor: Callable, jwt_controller: JwtTokenController):
        self.user_interactor = user_interactor
        self.jwt_controller = jwt_controller

    def method(self) -> str:
        return "auth.auth"

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        login_email = payload.obtrain_str('login')
        password = payload.obtrain_str('password')

        if login_email is None:
            return self.wrap_invalid_response("login parameter must be specified")
        if password is None:
            return self.wrap_invalid_response("password parameter must be specified")

        try:
            user = self.user_interactor.auth(login_email, password)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        if user is None:
            return self.wrap_invalid_response("Password or login is incorrect")

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

