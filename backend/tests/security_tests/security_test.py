import sys
sys.path.insert(0, "../../api")

import json
import unittest
from keys import *
from security import *
from jwt import JWT, jwk_from_dict

access_path = "../tools/certs/access_secret.json"
refresh_path = "../tools/certs/refresh_secret.json"


def create_jwt_controller() -> JwtTokenController:
    return JwtTokenControllerImpl(
        access_secret_file=access_path,
        refresh_secret_file=refresh_path
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


    def test_access_token_expiration(self):
        controller = create_jwt_controller()

    def test_creating_jwt_controller(self):
        controller = create_jwt_controller()

    def test_refresh_token_expiration(controller):
        controller = create_jwt_controller()

    def test_generating_token(controller):
        controller = create_jwt_controller()


def run():
    unittest.main()
