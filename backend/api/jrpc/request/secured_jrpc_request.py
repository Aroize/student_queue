from typing import Callable
from .jrpc_request import JRPCRequest
from ..exceptions import InvalidAccessCredentials


class SecuredJRPCRequest(JRPCRequest):

    def __init__(
        self,
        headers: dict,
        validator: Callable,
        other: JRPCRequest,
        need_valid_access_token: bool = True
    ):
        self.method = other.method
        self.params = other.params
        self.id = other.id

        credentials = validator.retreive_credentials(headers)

        if need_valid_access_token and not validator.is_access_token_valid(credentials):
            raise InvalidAccessCredentials

        self.credentials = credentials
