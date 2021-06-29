from keys import *
from jwt import JWT
from random import randint
from datetime import datetime, timedelta, timezone
from jwt.utils import get_time_from_int, get_int_from_datetime

# Data classes for credentials

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

# Interface for jwt generator and validator

class JwtTokenController:

    def retreive_credentials(self, headers: dict) -> Credentials:
        raise NotImplementedError("Not implemented")

    def is_access_token_valid(self, credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def is_refresh_token_valid(self, credentials: Credentials) -> bool:
        raise NotImplementedError("Not implemented")

    def generate_full_credentials(self, credentials: Credentials) -> RefreshCredentials:
        raise NotImplementedError("Not implemented")


# Implementation of jwt generator and validator


class JwtTokenControllerImpl(JwtTokenController):


    # TODO(): change signature from str to files
    def __init__(self, access_secret: str, refresh_secret: str):
        self.access_secret = access_secret
        self.refresh_secret = refresh_secret


    def retreive_credentials(self, headers: dict) -> Credentials:
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


    def __parse_jwt__(self, token: str, key: str) -> dict:
        instance = JWT()
        try:
            instance.decode(token, key, do_time_check=False)
        except Exception as e:
            return None


    def __is_token_expired__(self, token: dict) -> bool:
        time = token['exp']
        now = datetime.now(timezone.utc)

        exp = get_time_from_int(time)

        return now >= exp


    def __generate_access_token__(self, id: int, rcd: int) -> str:
        exp = get_int_from_datetime(
            datetime.now(timezone.utc) + timedelta(minutes=15)
        )
        message = {
            'sub': id,
            'rcd': rcd,
            'exp': exp
        }
        instance = JWT()
        return instance.encode(message, self.access_secret, alg='HS512')

    def __generate_refresh_token__(self, rcd: int) -> str:
        exp = get_int_from_datetime(
            datetime.now(timezone.utc) + timedelta(weeks=2)
        )
        message = {
            'sub': rcd,
            'exp': exp
        }
        instance = JWT()
        return instance.encode(message, self.refresh_secret, alg='HS512')
