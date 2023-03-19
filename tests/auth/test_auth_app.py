import unittest

import jwt
import responses
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from mojang.api.auth.models import MojangAuthenticationApp
from mojang.api.urls import (
    api_ms_xbl_authenticate,
    api_ms_xbl_authorize,
    api_ms_xbl_login,
    api_session_name_change,
    api_session_ownership,
    api_session_profile,
)
from mojang.exceptions import MicrosoftInvalidGrant

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


class TestAuthApp(unittest.TestCase):
    _skin_url = "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b"
    _uuid = "4ba22ce11f064d7f9f715634aa0d7973"
    _name = "Lucino772"
    _mc_token = "MINECRAFT_TOKEN"
    _refresh_token = "REFRESH_TOKEN"

    # Mocked MSAL App
    class _MockedMsalClientApplicationOk:
        def acquire_token_by_authorization_code(
            self, code, scopes, redirect_uri
        ):
            return {
                "error": False,
                "access_token": "ACCESS_TOKEN",
                "refresh_token": TestAuthApp._refresh_token,
            }

    class _MockedMsalClientApplicationInvalidGrant:
        def acquire_token_by_authorization_code(
            self, code, scopes, redirect_uri
        ):
            return {"error": True}

    # Mocked Responses
    def _mock_fetch_profile200(self):
        responses.add(
            method=responses.GET, url=self._skin_url, body=b"", status=200
        )
        responses.add(
            method=responses.GET,
            url=api_session_profile,
            json={
                "id": self._uuid,
                "name": self._name,
                "skins": [
                    {
                        "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                        "state": "ACTIVE",
                        "url": self._skin_url,
                        "variant": "CLASSIC",
                        "alias": "STEVE",
                    }
                ],
                "capes": [
                    {
                        "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                        "state": "ACTIVE",
                        "url": self._skin_url,
                    }
                ],
            },
            status=200,
        )
        responses.add(
            method=responses.GET,
            url=api_session_name_change,
            json={
                "createdAt": "2021-01-01T00:00:00Z",
                "nameChangeAllowed": True,
            },
            status=200,
        )

    def _mock_auth_xbl200(self):
        token, userhash = "TOKEN", "USERHASH"
        responses.add(
            method=responses.POST,
            url=api_ms_xbl_authenticate,
            json={
                "IssueInstant": "2020-12-07T19:52:08.4463796Z",
                "NotAfter": "2020-12-21T19:52:08.4463796Z",
                "Token": token,
                "DisplayClaims": {"xui": [{"uhs": userhash}]},
            },
            status=200,
        )

    def _mock_auth_xsts200(self):
        token, userhash = "TOKEN", "USERHASH"
        responses.add(
            method=responses.POST,
            url=api_ms_xbl_authorize,
            json={
                "IssueInstant": "2020-12-07T19:52:09.2345095Z",
                "NotAfter": "2020-12-08T11:52:09.2345095Z",
                "Token": token,
                "DisplayClaims": {"xui": [{"uhs": userhash}]},
            },
            status=200,
        )

    def _mock_auth_mc200(self):
        responses.add(
            method=responses.POST,
            url=api_ms_xbl_login,
            json={
                "username": "some uuid",
                "roles": [],
                "access_token": self._mc_token,
                "token_type": "Bearer",
                "expires_in": 86400,
            },
            status=200,
        )

    def _mock_owns_mc200(self):
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

    # Tests
    @responses.activate
    def test_get_session_ok(self):
        self._mock_fetch_profile200()
        self._mock_auth_xbl200()
        self._mock_auth_xsts200()
        self._mock_auth_mc200()
        self._mock_owns_mc200()

        app = MojangAuthenticationApp(
            TestAuthApp._MockedMsalClientApplicationOk(), "https://localhost"
        )
        self.assertIsNotNone(app.get_session("AUTH_CODE"))

    @responses.activate
    def test_get_session_invalid(self):
        self._mock_fetch_profile200()
        self._mock_auth_xbl200()
        self._mock_auth_xsts200()
        self._mock_auth_mc200()
        self._mock_owns_mc200()

        app = MojangAuthenticationApp(
            TestAuthApp._MockedMsalClientApplicationInvalidGrant(),
            "https://localhost",
        )
        self.assertRaises(MicrosoftInvalidGrant, app.get_session, "AUTH_CODE")
