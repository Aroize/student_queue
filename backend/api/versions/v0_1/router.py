from typing import Dict
import json
from tornado.web import RequestHandler
import inject
from backend.api.jrpc import JRPCRequest, SecuredJRPCRequest, JRPCErrorResponse
from backend.api.jrpc import InvalidRequestException, InvalidAccessCredentials
from backend.api.jrpc import JRPCErrorCodes
from backend.api.security import JwtTokenController
from .handlers import BaseHandler


class RouteHandler(RequestHandler):

    def initialize(self, methods_mapping: Dict[str, BaseHandler]):
        self.methods = methods_mapping

    @inject.params(jwt_controller=JwtTokenController)
    def post(self, jwt_controller: JwtTokenController = None):
        try:
            orig_payload = json.loads(self.request.body)
        except json.JSONDecodeError:
            error = JRPCErrorResponse(JRPCErrorCodes.InvalidRequest.value,
                                      "Fail to parse json message",
                                      0)
            return self.write(error.json)

        # Validate json message
        try:
            payload = JRPCRequest(orig_payload)
        except InvalidRequestException:
            error = JRPCErrorResponse(JRPCErrorCodes.InvalidRequest.value,
                                      "Message is not a jrpc message",
                                      JRPCRequest.get_id(orig_payload))
            return self.write(error.json)

        # Search real method handler
        method = payload.method
        if method not in self.methods:
            error = JRPCErrorResponse(JRPCErrorCodes.MethodNotFound.value,
                                      "Method not found",
                                      JRPCRequest.get_id(orig_payload))
            return self.write(error.json)

        # Delegate to real method handler
        handler = self.methods[method]

        # Checking for request credentials
        if handler.is_secured():
            error = None
            try:
                payload = SecuredJRPCRequest(
                    self.request.headers,
                    payload,
                    handler.need_access_token()
                )
            except InvalidAccessCredentials:
                error = JRPCErrorResponse(JRPCErrorCodes.AccessTokenExpired.value,
                                          "Method is secured, access token is expired or absent",
                                          JRPCRequest.get_id(orig_payload))
            except RuntimeError:
                error = JRPCErrorResponse(JRPCErrorCodes.AbsentUserIdentity.value,
                                          "Method is secured, at least must be provided user id",
                                          JRPCRequest.get_id(orig_payload))
            if error is not None:
                return self.write(error.json)

        # execute method
        result = handler.process(payload)

        return self.write(result.json)
