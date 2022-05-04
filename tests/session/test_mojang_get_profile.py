import unittest
from unittest import mock

from mojang.api import session
from mojang.api.models import Cape, Skin
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(VALID_ACCESS_TOKEN)


class TestMojangGetProfile(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.get_profile)
    def test_valid_token(self, mock_get: mock.MagicMock):
        profile = session.get_profile(VALID_ACCESS_TOKEN)
        self.assertEqual(profile.uuid, "4ba22ce11f064d7f9f715634aa0d7973")
        self.assertEqual(profile.name, "Lucino772")
        self.assertEqual(
            profile.skins,
            [
                Skin(
                    "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                    "CLASSIC",
                    "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "ACTIVE",
                )
            ],
        )
        self.assertEqual(
            profile.capes,
            [
                Cape(
                    "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                    "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "ACTIVE",
                )
            ],
        )

    @mock.patch("requests.get", side_effect=mock_server.get_profile)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.get_profile, INVALID_ACCESS_TOKEN
        )
