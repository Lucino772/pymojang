import datetime as dt
import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import Unauthorized

from .mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(VALID_ACCESS_TOKEN)


class TestMojangNameChange(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.user_name_change)
    def test_valid_token(self, mock_get: mock.MagicMock):
        res = session.get_user_name_change(VALID_ACCESS_TOKEN)
        self.assertEqual(res.allowed, True)
        self.assertEqual(
            res.created_at,
            dt.datetime.strptime("2021-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        )

    @mock.patch("requests.get", side_effect=mock_server.user_name_change)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized, session.get_user_name_change, INVALID_ACCESS_TOKEN
        )
