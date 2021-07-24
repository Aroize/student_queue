from ..base import BaseHandler
from backend.api.jrpc import JRPCRequest, BaseJRPCResponse, JRPCSuccessResponse


class EchoHandler(BaseHandler):

    def method(self) -> str:
        return "debug.echo"

    """Returns request as a result"""
    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
