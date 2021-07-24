from .credentials import Credentials
from .refresh_credentials import RefreshCredentials


class JwtTokenController:

    def retreive_credentials(self, headers: dict) -> Credentials:
        raise NotImplementedError("Not implemented")

    def is_access_token_valid(self, credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def is_refresh_token_valid(self, credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def generate_full_credentials(self, credentials: Credentials) -> RefreshCredentials:
        raise NotImplementedError("Not implemented")
