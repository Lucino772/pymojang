import unittest

import jwt
import responses
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from mojang.api import session
from mojang.api.urls import api_session_ownership
from mojang.exceptions import Unauthorized

private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=4096, backend=default_backend()
)
public_key = private_key.public_key()

private_pem = (
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    .decode("utf-8")
    .strip()
)

public_pem = (
    public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    .decode("utf-8")
    .strip()
)


class TestMojangOwnsMinecraft(unittest.TestCase):
    @responses.activate
    def test200(self):
        product_minecraft_sig = jwt.encode(
            {"signerId": "2535416586892404", "name": "product_minecraft"},
            private_key,
            algorithm="RS256",
        )
        game_minecraft_sig = jwt.encode(
            {"signerId": "2535416586892404", "name": "game_minecraft"},
            private_key,
            algorithm="RS256",
        )
        signature = jwt.encode(
            {
                "entitlements": [
                    {"name": "product_minecraft"},
                    {"name": "game_minecraft"},
                ],
                "signerId": "2535416586892404",
            },
            private_key,
            algorithm="RS256",
        )
        responses.add(
            method=responses.GET,
            url=api_session_ownership,
            json={
                "items": [
                    {
                        "name": "product_minecraft",
                        "signature": product_minecraft_sig,
                    },
                    {
                        "name": "game_minecraft",
                        "signature": game_minecraft_sig,
                    },
                ],
                "signature": signature,
                "keyId": "1",
            },
            status=200,
        )

        owned = session.owns_minecraft(
            "TOKEN", verify_sig=True, public_key=public_pem
        )
        self.assertTrue(owned)

    @responses.activate
    def test401(self):
        responses.add(
            method=responses.GET, url=api_session_ownership, status=401
        )

        self.assertRaises(Unauthorized, session.owns_minecraft, "TOKEN")
