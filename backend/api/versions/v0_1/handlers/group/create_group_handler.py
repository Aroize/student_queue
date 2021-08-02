import inject
from backend.api.jrpc import SecuredJRPCRequest
from backend.api.jrpc import BaseJRPCResponse, JRPCSuccessResponse
from backend.api.domain.group import GroupInteractor
from ..base import SecuredHandler


class CreateGroupHandler(SecuredHandler):
    def method(self) -> str:
        return "group.create"

    # FOR DEBUG
    def need_access_token(self) -> bool:
        return False

    @inject.params(group_interactor=GroupInteractor)
    def process(self, payload: SecuredJRPCRequest, group_interactor: GroupInteractor = None) -> BaseJRPCResponse:
        user_id = payload.credentials.id

        title = payload.obtain_str('title')
        if title is None:
            return self.wrap_invalid_response("Title of group must be specified")

        try:
            group = group_interactor.create(title, user_id)
        except Exception as e:
            return self.wrap_invalid_response(str(e))

        return JRPCSuccessResponse(group.values, payload.id)
