from pathlib import Path
import json
from jwt import JWT, AbstractJWKBase, jwk_from_dict
from random import randint
from datetime import timedelta
from jwt.utils import get_time_from_int, get_int_from_datetime
from backend.api.security.keys import HEADER_USER_ID, HEADER_ACCESS_TOKEN, HEADER_REFRESH_TOKEN
from .jwt_token_controller import JwtTokenController
from .now_date_time_provider import NowDateTimeProvider
from .credentials import Credentials
from .refresh_credentials import RefreshCredentials
from .access_credentials import AccessCredentials


class JwtTokenControllerImpl(JwtTokenController):

    def __init__(
            self,
            access_secret: AbstractJWKBase = None,
            refresh_secret: AbstractJWKBase = None,
            access_secret_file: Path = None,
            refresh_secret_file: Path = None,
            access_secret_json: dict = None,
            refresh_secret_json: dict = None,
            datetime_provider: NowDateTimeProvider = NowDateTimeProvider()
    ):

        self.datetime_provider = datetime_provider

        if access_secret_file is not None and refresh_secret_file is not None:
            with open(access_secret_file) as access:
                access_secret_json = json.load(access)
            with open(refresh_secret_file) as refresh:
                refresh_secret_json = json.load(refresh)

        if access_secret_json is not None and refresh_secret_json is not None:
            access_secret = jwk_from_dict(access_secret_json)
            refresh_secret = jwk_from_dict(refresh_secret_json)

        if access_secret is None or refresh_secret is None:
            raise RuntimeError("Secret keys for access and refresh tokens must be specified")

        self.access_secret = access_secret
        self.refresh_secret = refresh_secret

    def retreive_credentials(self, headers: dict) -> Credentials:
        if HEADER_USER_ID not in headers:
            raise RuntimeError("Credentials must contain at least user id")

        user_id = int(headers[HEADER_USER_ID])

        if HEADER_ACCESS_TOKEN not in headers:
            return Credentials(user_id)

        access_token = headers[HEADER_ACCESS_TOKEN]

        if HEADER_REFRESH_TOKEN not in headers:
            return AccessCredentials(access_token, user_id)

        refresh_token = headers[HEADER_REFRESH_TOKEN]
        return RefreshCredentials(refresh_token, access_token, user_id)

    def is_access_token_valid(self, credentials: Credentials) -> bool:
        if not isinstance(credentials, AccessCredentials):
            return False

        jwt = self.__parse_jwt__(credentials.access_token, self.access_secret)
        if jwt is None or 'sub' not in jwt or self.__is_token_expired__(jwt):
            return False

        return jwt['sub'] == credentials.id

    def is_refresh_token_valid(self, credentials: Credentials) -> bool:
        if not isinstance(credentials, RefreshCredentials):
            return False

        access_jwt = self.__parse_jwt__(credentials.access_token, self.access_secret)
        refresh_jwt = self.__parse_jwt__(credentials.refresh_token, self.refresh_secret)

        if access_jwt is None or refresh_jwt is None:
            return False

        if 'sub' not in access_jwt or access_jwt['sub'] != credentials.id:
            return False

        if self.__is_token_expired__(refresh_jwt):
            return False

        if 'rcd' not in access_jwt or 'sub' not in refresh_jwt:
            return False

        return access_jwt['rcd'] == refresh_jwt['sub']

    def generate_full_credentials(self, credentials: Credentials) -> RefreshCredentials:
        rcd = randint(0, 1024)
        access_token = self.__generate_access_token__(credentials.id, rcd)
        refresh_token = self.__generate_refresh_token__(rcd)
        return RefreshCredentials(refresh_token, access_token, credentials.id)

    def __parse_jwt__(self, token: str, key: AbstractJWKBase) -> dict:
        instance = JWT()
        try:
            return instance.decode(token, key, do_time_check=False)
        except Exception as e:
            return None

    def __is_token_expired__(self, token: dict) -> bool:
        time = token['exp']
        now = self.datetime_provider.now()

        exp = get_time_from_int(time)

        return now >= exp

    def __generate_access_token__(self, id: int, rcd: int) -> str:
        exp = get_int_from_datetime(
            self.datetime_provider.now() + timedelta(minutes=15)
        )
        message = {
            'sub': id,
            'rcd': rcd,
            'exp': exp
        }
        instance = JWT()
        return instance.encode(message, self.access_secret, alg='RS256')

    def __generate_refresh_token__(self, rcd: int) -> str:
        exp = get_int_from_datetime(
            self.datetime_provider.now() + timedelta(weeks=2)
        )
        message = {
            'sub': rcd,
            'exp': exp
        }
        instance = JWT()
        return instance.encode(message, self.refresh_secret, alg='RS256')
