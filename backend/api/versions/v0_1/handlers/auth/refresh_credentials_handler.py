from ..base import SecuredHandler
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.security import JwtTokenController


class RefreshCredentialsHandler(SecuredHandler):

    def __init__(self, jwt_controller: JwtTokenController):
        self.jwt_controller = jwt_controller

    def need_access_token(self) -> bool:
        return False

    def method(self) -> str:
        return "auth.refresh_credentials"

    def process(self, payload: SecuredJRPCRequest) -> BaseJRPCResponse:
        if not self.jwt_controller.is_refresh_token_valid(payload.credentials):
            return self.wrap_invalid_response("Refresh token is invalid or expired")

        refresh_creds = self.jwt_controller.generate_full_credentials(payload.credentials)

        response = {
            "access_token": refresh_creds.access_token,
            "refresh_token": refresh_creds.refresh_token
        }

        return JRPCSuccessResponse(response, payload.id)
