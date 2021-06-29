from .message import JRPCSuccessResponse, JRPCRequest



class BaseHandler:
    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse: # TODO: generalize
        raise NotImplementedError


class EchoHandler(BaseHandler):
    """Returns request as a result"""
    def process(self, payload: JRPCRequest) -> JRPCSuccessResponse:
        return JRPCSuccessResponse(payload.json, payload.id)
