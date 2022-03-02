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


class TestMojangCheckUsername(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.check_username)
    def test_available_name(self, mock_get: mock.MagicMock):
        self.assertEqual(
            session.check_username(VALID_ACCESS_TOKEN, "lucino"), True
        )

    @mock.patch("requests.get", side_effect=mock_server.check_username)
    def test_unavailable_name(self, mock_get: mock.MagicMock):
        self.assertEqual(
            session.check_username(VALID_ACCESS_TOKEN, "Notch"), False
        )

    @mock.patch("requests.get", side_effect=mock_server.check_username)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.check_username,
            INVALID_ACCESS_TOKEN,
            "lucino",
        )

    @mock.patch("requests.get", side_effect=mock_server.check_username_429)
    def test_too_many_requests(self, mock_get: mock.MagicMock):
        self.assertRaises(
            RuntimeError, session.check_username, VALID_ACCESS_TOKEN, "lucino"
        )
