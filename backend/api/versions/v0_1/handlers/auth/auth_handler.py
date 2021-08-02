import inject
from backend.api.jrpc import BaseJRPCResponse, JRPCRequest, JRPCSuccessResponse
from backend.api.security import JwtTokenControllerImpl, Credentials
from backend.api.domain import UserInteractor
from ..base import BaseHandler


class AuthHandler(BaseHandler):
    def method(self) -> str:
        return "auth.auth"

    @inject.params(user_interactor=UserInteractor,
                   jwt_controller=JwtTokenControllerImpl)
    def process(self,
                payload: JRPCRequest,
                user_interactor: UserInteractor = None,
                jwt_controller: JwtTokenControllerImpl = None) -> BaseJRPCResponse:
        login_email = payload.obtain_str('login')
        password = payload.obtain_str('password')

        if login_email is None:
            return self.wrap_invalid_response("login parameter must be specified")
        if password is None:
            return self.wrap_invalid_response("password parameter must be specified")

        try:
            user = user_interactor.auth(login_email, password)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        if user is None:
            return self.wrap_invalid_response("Password or login is incorrect")

        base_credentials = Credentials(user.id)
        full_credentials = jwt_controller.generate_full_credentials(base_credentials)

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
