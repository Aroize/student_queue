import json
from loguru import logger
from tornado.web import RequestHandler
from typing import Union, Callable, Dict
from .message import JRPCRequest, SecuredJRPCRequest, JRPCErrorResponse
from .exceptions import InvalidRequestException, InvalidAccessCredentials
from .exceptions import JRPCErrorCode, InvalidParametersException


class RouteHandler(RequestHandler):


    def initialize(self, methods: Dict[str, Callable], jwt_controller: Callable):
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
            error = None
            try:
                payload = SecuredJRPCRequest(
                    self.request.headers,
                    self.jwt_controller,
                    payload,
                    handler.need_access_token()
                )
            except InvalidAccessCredentials:
                error = JRPCErrorResponse(JRPCErrorCode.AccessTokenExpired.value,
                                          "Method is secured, access token is expired or absent",
                                          JRPCRequest.get_id(orig_payload))
            except RuntimeError:
                error = JRPCErrorResponse(JRPCErrorCode.AbsentUserIdentity.value,
                                          "Method is secured, at least must be provided user id",
                                          JRPCRequest.get_id(orig_payload))
            if error is not None:
                return self.write(error.json)

        # execute method
        result = handler.process(payload)

        return self.write(result.json)


class EmailVerificationHandler(RequestHandler):

    def initialize(self, user_interactor: Callable):
        self.user_interactor = user_interactor

    def get(self):
        id = int(self.get_argument('id'))
        code = int(self.get_argument('code'))

        logger.info("called verify_email with id = {} and code = {}".format(id, code))

        if id is None or code is None:
            self.redirect('/res/html/failed.html')
        elif self.user_interactor.confirm_email(id, code):
            self.redirect('/res/html/success.html')
        else:
            self.redirect('/res/html/failed.html')

        return
