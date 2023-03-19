import unittest

import responses

from mojang.api.auth.models import MicrosoftAuthenticatedUser
from mojang.api.urls import (
    api_ms_xbl_authenticate,
    api_ms_xbl_authorize,
    api_ms_xbl_login,
    api_session_name_change,
    api_session_profile,
)


class TestAuthUser(unittest.TestCase):
    _skin_url = "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b"
    _uuid = "4ba22ce11f064d7f9f715634aa0d7973"
    _name = "Lucino772"
    _mc_token = "MINECRAFT_TOKEN"
    _refresh_token = "REFRESH_TOKEN"

    class _MockedMsalClientApplication:
        def acquire_token_by_refresh_token(self, refresh_token, scopes):
            return {
                "access_token": "ACCESS_TOKEN",
                "refresh_token": TestAuthUser._refresh_token,
            }

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

    @responses.activate
    def test_fetch_profile(self):
        self._mock_fetch_profile200()
        user = MicrosoftAuthenticatedUser(
            "ACCESS_TOKEN",
            "REFRESH_TOKEN",
            TestAuthUser._MockedMsalClientApplication(),
        )

        self.assertEqual(user.name, self._name)
        self.assertEqual(user.uuid, self._uuid)
        self.assertFalse(user.is_legacy)
        self.assertFalse(user.is_demo)
        self.assertIsNotNone(user.skins)
        self.assertIsNotNone(user.skin)
        self.assertIsNotNone(user.capes)
        self.assertIsNotNone(user.cape)
        self.assertTrue(user.name_change_allowed)
        self.assertIsNotNone(user.created_at)

    @responses.activate
    def test_refresh_close(self):
        self._mock_fetch_profile200()
        self._mock_auth_xbl200()
        self._mock_auth_xsts200()
        self._mock_auth_mc200()

        user = MicrosoftAuthenticatedUser(
            "ACCESS_TOKEN",
            "REFRESH_TOKEN",
            TestAuthUser._MockedMsalClientApplication(),
        )

        self.assertEqual(user._access_token, "ACCESS_TOKEN")
        self.assertEqual(user._refresh_token, "REFRESH_TOKEN")
        user.refresh()
        self.assertEqual(user._access_token, self._mc_token)
        self.assertEqual(user._refresh_token, self._refresh_token)
        user.close()
        self.assertIsNone(user._access_token)
        self.assertIsNone(user._refresh_token)
