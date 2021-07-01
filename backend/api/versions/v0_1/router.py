from typing import Union, Callable, Dict
import json
from tornado.web import RequestHandler
from .message import JRPCRequest
from .exceptions import InvalidRequestException
from .exceptions import JRPCErrorCode



class JRPCErrorResponse(dict):
    """Creates serializable error response"""
    def __init__(self, code: int, message: str, id: int=None):
        # TODO: move to messages
        self._response = {"jsonrpc": "2.0",
                          "error": {
                              "code": code,
                              "message": message},
                          "id": id}

    @property
    def json(self):
        return self._response



class RouteHandler(RequestHandler):
    """jRPC application entry point. Routes requests to real handlers"""

    def initialize(self, methods: Dict[str, Callable], jwt_controller: Callable):
        """Initializes router with real handlers"""
        self.methods = methods
        self.jwt_controller = jwt_controller

    def post(self):
        orig_payload = json.loads(self.request.body)

        # Validate json message
        try:
            payload = JRPCRequest(orig_payload)
        except InvalidRequestException:
            self.set_status(400)
            error = JRPCErrorResponse(JRPCErrorCode.InvalidRequest.value,
                                      "Message is not a jrpc message",
                                      JRPCRequest.get_id(orig_payload))
            return self.write(error.json)

        # Search real method handler
        method = payload.method
        if method not in self.methods:
            self.set_status(400)
            error = JRPCErrorResponse(JRPCErrorCode.MethodNotFound.value,
                                      "Method not found",
                                      JRPCRequest.get_id(orig_payload))
            return self.write(error.json)

        # Delegate to real method handler
        handler = self.methods[method]

        # Checking for request credentials
        if handler.is_secured():
            headers = self.request.headers
            error = None
            credentials = None
            try:
                credentials = self.jwt_controller.retreive_credentials(headers)
            except RuntimeError:
                error = JRPCErrorResponse(JRPCErrorCode.AbsentUserIdentity.value,
                                          "Method is secured, at least must be provided user id",
                                          JRPCRequest.get_id(orig_payload))
            if credentials is not None and not self.jwt_controller.is_access_token_valid(credentials):
                error = JRPCErrorResponse(JRPCErrorCode.AccessTokenExpired.value,
                                          "Method is secured, access token is expired or absent",
                                          JRPCRequest.get_id(orig_payload))

            if error is not None:
                return self.write(error.json)


        result = handler.process(payload)

        return self.write(result.json)
