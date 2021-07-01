from versions.v0_1.message import JRPCSuccessResponse, JRPCRequest

class BaseHandler:

    def is_secured(self) -> bool:
        return False

    def method(self) -> str:
        raise NotImplementedError

    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse: # TODO: generalize
        raise NotImplementedError


class SecuredHandler(BaseHandler):

    def is_secured(self) -> bool:
        return True


class EchoHandler(BaseHandler):

    def method(self) -> str:
        return "debug.echo"

    """Returns request as a result"""
    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse:
        return JRPCSuccessResponse(payload.json, payload.id)


class SecuredEchoHandler(SecuredHandler):

    def method(self) -> str:
        return "debug.echo_secured"

    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
