from versions.v0_1.message import JRPCSuccessResponse, JRPCRequest

class BaseHandler:

    def method(self) -> str:
        raise NotImplementedError

    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse: # TODO: generalize
        raise NotImplementedError


class EchoHandler(BaseHandler):

    def method(self) -> str:
        return "debug.echo"

    """Returns request as a result"""
    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
