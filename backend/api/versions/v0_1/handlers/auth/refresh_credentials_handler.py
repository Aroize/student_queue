import inject
from backend.api.jrpc import BaseJRPCResponse, SecuredJRPCRequest, JRPCSuccessResponse
from backend.api.security import JwtTokenController
from ..base import SecuredHandler


class RefreshCredentialsHandler(SecuredHandler):
    def need_access_token(self) -> bool:
        return False

    def method(self) -> str:
        return "auth.refresh_credentials"

    @inject.params(jwt_controller=JwtTokenController)
    def process(self, payload: SecuredJRPCRequest, jwt_controller: JwtTokenController = None) -> BaseJRPCResponse:
        if not jwt_controller.is_refresh_token_valid(payload.credentials):
            return self.wrap_invalid_response("Refresh token is invalid or expired")

        refresh_creds = jwt_controller.generate_full_credentials(payload.credentials)

        response = {
            "access_token": refresh_creds.access_token,
            "refresh_token": refresh_creds.refresh_token
        }

        return JRPCSuccessResponse(response, payload.id)
