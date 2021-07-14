from typing import Callable
from .base_handlers import BaseHandler
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse, JRPCRequest
from versions.v0_1.exceptions import JRPCErrorCode


class ListUsersHandler(BaseHandler):
    """Handler for listing users data in debug web interface"""

    def __init__(self, user_interactor: Callable):
        self.user_interactor = user_interactor

    def method(self) -> str:
        return "debug.users.list"

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        users = self.user_interactor.list()

        return JRPCSuccessResponse(users, payload.id)
