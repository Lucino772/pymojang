import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(
    VALID_ACCESS_TOKEN, unavailable_names=["Notch"]
)


class TestMojangChangeSkin(unittest.TestCase):
    @mock.patch("requests.post", side_effect=mock_server.change_user_skin)
    def test_valid_token(self, mock_post: mock.MagicMock):
        ok = session.change_user_skin(
            VALID_ACCESS_TOKEN,
            "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680",
        )
        self.assertEqual(ok, True)

    @mock.patch("requests.post", side_effect=mock_server.change_user_skin)
    def test_invalid_token(self, mock_post: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.change_user_skin,
            INVALID_ACCESS_TOKEN,
            "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680",
        )
