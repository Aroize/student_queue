import json
import sys
import unittest

from jwt import JWT, jwk_from_dict
sys.path.insert(0, "../api")
from keys import *
from security import *


def create_jwt_controller():
    return True



class SecurityTests(unittest.TestCase):
    def test_creating_jwt_controller(self):
        controller = create_jwt_controller()

        access_path = "../tools/certs/access_secret.json"
        refresh_path = "../tools/certs/refresh_secret.json"

        from_path = JwtTokenControllerImpl(
            access_secret_file=access_path,
            refresh_secret_file=refresh_path
        )

        assert from_path.access_secret is not None
        assert from_path.refresh_secret is not None

        print("successfully created from path...")

        access_dict = json.load(open(access_path))
        refresh_dict = json.load(open(refresh_path))

        from_dict = JwtTokenControllerImpl(
            access_secret_json=access_dict,
            refresh_secret_json=refresh_dict
        )

        assert from_dict.access_secret is not None
        assert from_dict.refresh_secret is not None

        print("successfully created from json...")

        access_secret = jwk_from_dict(access_dict)
        refresh_secret = jwk_from_dict(refresh_dict)

        from_jwk = JwtTokenControllerImpl(
            access_secret=access_secret,
            refresh_secret=refresh_secret
        )

        assert from_jwk.access_secret is not None
        assert from_jwk.refresh_secret is not None

        print("successfully created from jwk...")

        print("<== finished test: creation of jwt controller ==>\n")

    def test_access_token_expiration(self):
        controller = create_jwt_controller()

    def test_creating_jwt_controller():
        controller = create_jwt_controller()

    def test_refresh_token_expiration(controller):
        controller = create_jwt_controller()

    def test_generating_token(controller):
        controller = create_jwt_controller()
