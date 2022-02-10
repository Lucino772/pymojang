import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(VALID_ACCESS_TOKEN)


class TestMojangResetSkin(unittest.TestCase):
    @mock.patch("requests.delete", side_effect=mock_server.reset_user_skin)
    def test_valid_token(self, mock_delete: mock.MagicMock):
        ok = session.reset_user_skin(VALID_ACCESS_TOKEN)
        self.assertEqual(ok, True)

    @mock.patch("requests.delete", side_effect=mock_server.reset_user_skin)
    def test_invalid_token(self, mock_delete: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.reset_user_skin, INVALID_ACCESS_TOKEN
        )
