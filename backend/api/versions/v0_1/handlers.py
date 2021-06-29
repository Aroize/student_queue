from typing import Union
import json
from enum import Enum
from tornado.web import RequestHandler



class JRPCError(Enum):
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParameters = -32602
    InternalError = -32603
    ServerError = -32000


class JRPCErrorResponse(dict):
    def __init__(self, code: int, message: str, id: int=None):
        self._response = {"jsonrpc": "2.0",
                          "error": {
                              "code": code,
                              "message": message},
                          "id": id}

    @property
    def response(self):
        return self._response



class RouteHandler(RequestHandler):

    def initialize(self, methods: List[])

    def _is_jrpc_call(self, jmsg: dict) -> bool:
        if len(jmsg.keys()) in (3, 4):
            return False
        if "jsonrpc" not in jmsg.keys() or
           "method"      in jmsg.keys() or
           "params"      in jmgs.keys() or
           "id"          in jmsg.keys():
           return False
        else:
           return True

    def _get_id(self, payload: dict) -> Union[dict, None]:
        return None if "id" not in payload.keys() else payload["id"]

    def post(self):
        payload = json.loads(self.request.body)

        # Validate json message
        if not self._is_jrpc_call(payload):
            self.set_status(400)
            error = JRPCErrorResponse(JRPCError.InvalidRequest,
                                      "Message is not a jrpc message",
                                      self._get_id(payload))
            return self.write(error))

        # Search real method handler
        method = payload["method"]
        if method not in self.methods:
            self.set_status(400)
            error = JRPCErrorResponse(JRPCError.MethodNotFound,
                                      "Method not found",
                                      self._get_id(payload))
            return self.write(error)

        # Delegate to real method handler
        raise NotImplementedError

        return self.write(payload)
