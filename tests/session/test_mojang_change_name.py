import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import InvalidName, Unauthorized, UnavailableName
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(
    VALID_ACCESS_TOKEN, unavailable_names=["Notch"]
)


class TestMojangChangeName(unittest.TestCase):
    @mock.patch("requests.put", side_effect=mock_server.change_user_name)
    def test_valid_token(self, mock_put: mock.MagicMock):
        ok = session.change_user_name(VALID_ACCESS_TOKEN, "lucino")
        self.assertEqual(ok, True)

    @mock.patch("requests.put", side_effect=mock_server.change_user_name)
    def test_invalid_token(self, mock_put: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.change_user_name,
            INVALID_ACCESS_TOKEN,
            "lucino",
        )

    @mock.patch("requests.put", side_effect=mock_server.change_user_name)
    def test_invalid_name(self, mock_put: mock.MagicMock):
        self.assertRaises(
            InvalidName,
            session.change_user_name,
            VALID_ACCESS_TOKEN,
            "xxxxxxxxxxxxxxxxx",
        )

    @mock.patch("requests.put", side_effect=mock_server.change_user_name)
    def test_unavailable_name(self, mock_put: mock.MagicMock):
        self.assertRaises(
            UnavailableName,
            session.change_user_name,
            VALID_ACCESS_TOKEN,
            "Notch",
        )
