import sys
sys.path.insert(0, "../../api")

import json
import unittest
from keys import *
from security import *
from datetime import datetime, timezone, timedelta
from jwt import JWT, jwk_from_dict

access_path = "backend/tools/certs/access_secret.json"
refresh_path = "backend/tools/certs/refresh_secret.json"


class TestNowDateTimeProvider(NowDateTimeProvider):

    def __init__(self, delta: timedelta):
        self.delta = delta

    def now(self) -> datetime:
        return super().now() - self.delta


def create_jwt_controller() -> JwtTokenController:
    return JwtTokenControllerImpl(
        access_secret_file=access_path,
        refresh_secret_file=refresh_path
    )

def create_fake_jwt_controller(timedelta: timedelta) -> JwtTokenController:
    return JwtTokenControllerImpl(
        access_secret_file=access_path,
        refresh_secret_file=refresh_path,
        datetime_provider=TestNowDateTimeProvider(timedelta)
    )


class SecurityTests(unittest.TestCase):

    def test_creating_jwt_controller(self):

        from_path = JwtTokenControllerImpl(
            access_secret_file=access_path,
            refresh_secret_file=refresh_path
        )

        self.assertIsNotNone(from_path.access_secret)
        self.assertIsNotNone(from_path.refresh_secret)

        with open(access_path) as access:
            access_dict = json.load(access)

        with open(refresh_path) as refresh:
            refresh_dict = json.load(refresh)

        from_dict = JwtTokenControllerImpl(
            access_secret_json=access_dict,
            refresh_secret_json=refresh_dict
        )

        self.assertIsNotNone(from_dict.access_secret)
        self.assertIsNotNone(from_dict.refresh_secret)

        access_secret = jwk_from_dict(access_dict)
        refresh_secret = jwk_from_dict(refresh_dict)

        from_jwk = JwtTokenControllerImpl(
            access_secret=access_secret,
            refresh_secret=refresh_secret
        )

        self.assertIsNotNone(from_jwk.access_secret)
        self.assertIsNotNone(from_jwk.refresh_secret)

    def test_retrieving_credentials(self):
        controller = create_jwt_controller()

        headers = {}

        with self.assertRaises(RuntimeError):
            controller.retreive_credentials(headers)

        uid = 111
        headers[HEADER_USER_ID] = uid
        creds = controller.retreive_credentials(headers)
        self.assertIsInstance(creds, Credentials)
        self.assertEquals(creds.id, uid)

        fake_access_token = "qwertyuiop"
        headers[HEADER_ACCESS_TOKEN] = fake_access_token
        creds = controller.retreive_credentials(headers)
        self.assertIsInstance(creds, AccessCredentials)
        self.assertEquals(creds.id, uid)
        self.assertEquals(creds.access_token, fake_access_token)

        fake_refresh_token = "asdfghjkl"
        headers[HEADER_REFRESH_TOKEN] = fake_refresh_token
        creds = controller.retreive_credentials(headers)
        self.assertIsInstance(creds, RefreshCredentials)
        self.assertEquals(creds.id, uid)
        self.assertEquals(creds.access_token, fake_access_token)
        self.assertEquals(creds.refresh_token, fake_refresh_token)


    def test_generating_token(self):
        controller = create_jwt_controller()

        fake_credentials = Credentials(1)
        fake_refresh_credentials = controller.generate_full_credentials(fake_credentials)

        self.assertTrue(controller.is_access_token_valid(fake_refresh_credentials))
        self.assertTrue(controller.is_refresh_token_valid(fake_refresh_credentials))


    def test_access_token_expiration(self):

        expired_controller = create_fake_jwt_controller(timedelta(minutes=20))
        fake_credentials = Credentials(1)
        expired_credentials = expired_controller.generate_full_credentials(fake_credentials)

        controller = create_jwt_controller()
        self.assertFalse(controller.is_access_token_valid())


    def test_refresh_token_expiration(self):
        expired_controller = create_fake_jwt_controller(timedelta(weeks=3))
        fake_credentials = Credentials(1)
        expired_credentials = expired_controller.generate_full_credentials(fake_credentials)

        controller = create_jwt_controller()
        self.assertFalse(controller.is_refresh_token_valid(expired_credentials))


def run():
    unittest.main()
