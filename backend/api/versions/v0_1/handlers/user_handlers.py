from typing import Callable
from .base_handlers import BaseHandler, SecuredHandler
from versions.v0_1.message import JRPCRequest, SecuredJRPCRequest
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse


class GetUserHandler(SecuredHandler):

    def __init__(self, user_repository: Callable):
        self.user_repository = user_repository

    def method(self) -> str:
        return "user.get"

    def process(self, payload: SecuredJRPCRequest) -> BaseJRPCResponse:

        user_id = payload.obtrain_param('id')
        if user_id is None:
            return self.wrap_invalid_response("User id must be specified")

        user_id = int(user_id)

        try:
            user = self.user_repository.find_user_by_id(user_id)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse(user.json(), payload.id)
