import inject
from backend.api.security import JwtTokenControllerImpl
from .jrpc_request import JRPCRequest
from ..exceptions import InvalidAccessCredentials


class SecuredJRPCRequest(JRPCRequest):

    @inject.params(validator=JwtTokenControllerImpl)
    def __init__(
        self,
        headers: dict,
        other: JRPCRequest,
        need_valid_access_token: bool = True,
        validator: JwtTokenControllerImpl = None
    ):
        self.method = other.method
        self.params = other.params
        self.id = other.id

        credentials = validator.retreive_credentials(headers)

        if need_valid_access_token and not validator.is_access_token_valid(credentials):
            raise InvalidAccessCredentials

        self.credentials = credentials
