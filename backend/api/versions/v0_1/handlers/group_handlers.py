from typing import Callable
from .base_handlers import BaseHandler, SecuredHandler
from versions.v0_1.message import JRPCRequest, SecuredJRPCRequest
from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse


class CreateGroupHandler(SecuredHandler):

    def __init__(self, group_interactor: Callable):
        self.group_interactor = group_interactor

    def method(self) -> str:
        return "group.create"

    # FOR DEBUG ONLY
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


class ListGroupHandler(SecuredHandler):

    def __init__(self, group_interactor: Callable):
        self.group_interactor = group_interactor

    def method(self) -> str:
        return "group.list"

    # FOR DEBUG ONLY
    def need_access_token(self) -> bool:
        return False

    def process(self, payload: SecuredJRPCRequest) -> BaseJRPCResponse:
        group_id = payload.obtrain_param('id')
        offset = payload.obtrain_param('offset', 0)
        count = payload.obtrain_param('count', 20)

        if group_id is None:
            return self.wrap_invalid_response("Group id must be specified")
        group_id = int(group_id)
        if offset < 0:
            return self.wrap_invalid_response("Offset can't be negative value")
        if count <= 0:
            return self.wrap_invalid_response("Count must be positive value")

        user_id = payload.credentials.id

        if not self.group_interactor.is_member(group_id, user_id):
            return self.wrap_invalid_response("You must be a member of group to list it's members")

        count, members = self.group_interactor.list_group(group_id, offset, count)

        response = {
            "count": count,
            "members": list(map(lambda user: user.json(), members))
        }

        return JRPCSuccessResponse(response, payload.id)
