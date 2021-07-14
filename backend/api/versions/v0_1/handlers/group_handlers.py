from typing import Callable
from .base_handlers import BaseHandler, SecuredHandler
from versions.v0_1.message import JRPCRequest, SecuredJRPCRequest
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse


class CreateGroupHandler(SecuredHandler):

    def __init__(self, group_interactor: Callable):
        self.group_interactor = group_interactor

    def method(self) -> str:
        return "group.create"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    def process(self, payload: SecuredJRPCRequest) -> BaseJRPCResponse:
        user_id = payload.credentials.id

        title = payload.obtrain_param('title')
        if title is None:
            return self.wrap_invalid_response("Title of group must be specified")

        try:
            group = self.group_interactor.create(title, user_id)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse(group.values, payload.id)