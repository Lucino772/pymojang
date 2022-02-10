import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(VALID_ACCESS_TOKEN)


class TestMojangHideCape(unittest.TestCase):
    @mock.patch("requests.delete", side_effect=mock_server.hide_user_cape)
    def test_valid_token(self, mock_delete: mock.MagicMock):
        ok = session.hide_user_cape(VALID_ACCESS_TOKEN)
        self.assertEqual(ok, True)

    @mock.patch("requests.delete", side_effect=mock_server.hide_user_cape)
    def test_invalid_token(self, mock_delete: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.hide_user_cape, INVALID_ACCESS_TOKEN
        )
