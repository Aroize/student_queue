from versions.v0_1.message import BaseJRPCResponse, JRPCErrorResponse, JRPCSuccessResponse, JRPCRequest
from versions.v0_1.exceptions import JRPCErrorCode


class BaseHandler:

    def is_secured(self) -> bool:
        return False

    def method(self) -> str:
        raise NotImplementedError

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:  # TODO: generalize
        raise NotImplementedError

    def wrap_invalid_response(self, message: str) -> JRPCErrorResponse:
        return JRPCErrorResponse(
            JRPCErrorCode.InvalidParameters.value,
            message,
            None
        )

    def __repr__(self):
        return f"Endpoint {self.method()}"


class SecuredHandler(BaseHandler):

    def is_secured(self) -> bool:
        return True

    def need_access_token(self) -> bool:
        return True


class EchoHandler(BaseHandler):

    def method(self) -> str:
        return "debug.echo"

    """Returns request as a result"""
    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        return JRPCSuccessResponse(payload.json, payload.id)


class SecuredEchoHandler(SecuredHandler):

    def method(self) -> str:
        return "debug.echo_secured"

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
