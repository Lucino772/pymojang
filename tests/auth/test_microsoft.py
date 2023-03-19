import unittest

import responses

from mojang.api.auth.microsoft import (
    authenticate_minecraft,
    authenticate_xbl,
    authenticate_xsts,
)
from mojang.api.urls import (
    api_ms_xbl_authenticate,
    api_ms_xbl_authorize,
    api_ms_xbl_login,
)
from mojang.exceptions import (
    Unauthorized,
    XboxLiveAuthenticationError,
    XboxLiveInvalidUserHash,
)


class TestMicrosoftAuth(unittest.TestCase):
    @responses.activate
    def test_auth_xbl200(self):
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
        ret = authenticate_xbl("RPS_TOKEN")
        self.assertEqual(ret[0], token)
        self.assertEqual(ret[1], userhash)

    @responses.activate
    def test_auth_xbl400(self):
        responses.add(
            method=responses.POST, url=api_ms_xbl_authenticate, status=400
        )
        self.assertRaises(
            XboxLiveAuthenticationError, authenticate_xbl, "RPS_TOKEN"
        )

    @responses.activate
    def test_auth_xsts200(self):
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
        ret = authenticate_xsts("XBL_TOKEN")
        self.assertEqual(ret[0], token)
        self.assertEqual(ret[1], userhash)

    @responses.activate
    def test_auth_xsts400(self):
        responses.add(
            method=responses.POST, url=api_ms_xbl_authorize, status=400
        )
        self.assertRaises(
            XboxLiveAuthenticationError, authenticate_xsts, "XBL_TOKEN"
        )

    @responses.activate
    def test_auth_mc200(self):
        token = "TOKEN"
        responses.add(
            method=responses.POST,
            url=api_ms_xbl_login,
            json={
                "username": "some uuid",
                "roles": [],
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 86400,
            },
            status=200,
        )
        self.assertEqual(
            authenticate_minecraft("USERHASH", "XSTS_TOKEN"), token
        )

    @responses.activate
    def test_auth_mc400(self):
        responses.add(method=responses.POST, url=api_ms_xbl_login, status=400)
        self.assertRaises(
            XboxLiveInvalidUserHash,
            authenticate_minecraft,
            "USERHASH",
            "XSTS_TOKEN",
        )

    @responses.activate
    def test_auth_mc401(self):
        responses.add(method=responses.POST, url=api_ms_xbl_login, status=401)
        self.assertRaises(
            Unauthorized, authenticate_minecraft, "USERHASH", "XSTS_TOKEN"
        )
