from ..base import SecuredHandler
from backend.api.jrpc import JRPCRequest, BaseJRPCResponse, JRPCSuccessResponse


class SecuredEchoHandler(SecuredHandler):

    def method(self) -> str:
        return "debug.echo_secured"

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
