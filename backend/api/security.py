from keys import *

class Credentials:

    def __init__(self, id: int):
        self.id = id


class AccessCredentials(Credentials):

    def __init__(self, access_token: str, id: int):
        super().__init__(id)
        self.access_token = access_token


class RefreshCredentials(AccessCredentials):

    def __init__(self, refresh_token: str, access_token: str, id: int):
        super().__init__(access_token, id)
        self.refresh_token = refresh_token



class JwtTokenController:

    def retreive_credentials(headers: dict) -> Credentials:
        raise NotImplementedError("Not implemented")

    def is_access_token_valid(credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def is_refresh_token_valid(credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def generate_full_credentials(credentials: Credentials) -> RefreshCredentials:
        raise NotImplementedError("Not implemented")





class JwtTokenControllerImpl(JwtTokenController):

    def retreive_credentials(headers: dict) -> Credentials:
        if HEADER_USER_ID not in headers:
            raise RuntimeError("Credentials must contain at least user id")

        user_id = headers[HEADER_USER_ID]

        if HEADER_ACCESS_TOKEN not in headers:
            return Credentials(user_id)

        access_token = headers[HEADER_ACCESS_TOKEN]

        if HEADER_REFRESH_TOKEN not in headers:
            return AccessCredentials(access_token, user_id)

        refresh_token = headers[HEADER_REFRESH_TOKEN]
        return RefreshCredentials(refresh_token, access_token, user_id)


    def is_access_token_valid(credentials: Credentials) -> bool:
        if not isinstance(credentials, AccessCredentials):
            return False

        
