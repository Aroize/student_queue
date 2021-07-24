from .access_credentials import AccessCredentials


class RefreshCredentials(AccessCredentials):

    def __init__(self, refresh_token: str, access_token: str, id: int):
        super().__init__(access_token, id)
        self.refresh_token = refresh_token
