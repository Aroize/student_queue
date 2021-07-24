from .credentials import Credentials


class AccessCredentials(Credentials):

    def __init__(self, access_token: str, id: int):
        super().__init__(id)
        self.access_token = access_token
