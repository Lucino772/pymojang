import unittest
from unittest import mock
from mojang.account import session
from mojang.exceptions import Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(VALID_ACCESS_TOKEN)


class TestMojangOwnsMinecraft(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.owns_minecraft)
    def test_valid_token(self, mock_get: mock.MagicMock):
        ok = session.owns_minecraft(VALID_ACCESS_TOKEN)
        self.assertEqual(ok, True)

    @mock.patch("requests.get", side_effect=mock_server.owns_minecraft)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.owns_minecraft, INVALID_ACCESS_TOKEN
        )
