from backend.api.jrpc import BaseJRPCResponse, JRPCErrorResponse, JRPCRequest
from backend.api.jrpc import JRPCErrorCodes


class BaseHandler:

    def is_secured(self) -> bool:
        return False

    def method(self) -> str:
        raise NotImplementedError

    def process(self, payload: JRPCRequest) -> BaseJRPCResponse:  # TODO: generalize
        raise NotImplementedError

    def wrap_invalid_response(self, message: str) -> JRPCErrorResponse:
        return JRPCErrorResponse(
            JRPCErrorCodes.InvalidParameters.value,
            message,
            None
        )

    def __repr__(self):
        return f"Endpoint {self.method()}"
