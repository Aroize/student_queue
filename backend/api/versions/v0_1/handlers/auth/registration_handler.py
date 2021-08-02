import inject
from backend.api.jrpc import BaseJRPCResponse, JRPCRequest, JRPCSuccessResponse
from backend.api.jrpc import JRPCErrorCodes, JRPCErrorResponse
from backend.api.domain import UserInteractor
from ..base import BaseHandler


class RegistrationHandler(BaseHandler):

    def method(self) -> str:
        return "auth.register"

    @inject.params(user_interactor=UserInteractor)
    def process(self, payload: JRPCRequest,
                user_interactor: UserInteractor = None) -> BaseJRPCResponse:
        login = payload.obtain_str('login')
        name = payload.obtain_str('name')
        surname = payload.obtain_str('surname')
        password = payload.obtain_str('password')
        email = payload.obtain_str('email')

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
            user = user_interactor.create(login, password, email, name, surname)
        except ValueError as e:
            return self.wrap_invalid_response(str(e))
        except RuntimeError as e:
            msg = str(e)
            return JRPCErrorResponse(
                JRPCErrorCodes.EntityAlreadyExists.value,
                msg,
                payload.id
            )
        except Exception as e:
            print(e)
            return JRPCErrorResponse(
                JRPCErrorCodes.InternalError.value,
                "Exception thrown during inserting into database",
                payload.id
            )

        # user must be specified
        user_json = user.json()

        return JRPCSuccessResponse(user_json, payload.id)
