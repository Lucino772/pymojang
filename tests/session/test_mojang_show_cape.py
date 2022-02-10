import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import NotCapeOwner, Unauthorized
from tests.session.mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

VALID_CAPE_ID = "THIS_IS_MY_CAPE"
INVALID_CAPE_ID = "THIS_IS_NOT_MY_CAPE"

mock_server = MockSessionServer(
    VALID_ACCESS_TOKEN, valid_cape_ids=[VALID_CAPE_ID]
)


class TestMojangShowCape(unittest.TestCase):
    @mock.patch("requests.put", side_effect=mock_server.show_user_cape)
    def test_valid_token(self, mock_put: mock.MagicMock):
        ok = session.show_user_cape(VALID_ACCESS_TOKEN, VALID_CAPE_ID)
        self.assertEqual(ok, True)

    @mock.patch("requests.put", side_effect=mock_server.show_user_cape)
    def test_invalid_token(self, mock_put: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.show_user_cape,
            INVALID_ACCESS_TOKEN,
            VALID_CAPE_ID,
        )

    @mock.patch("requests.put", side_effect=mock_server.show_user_cape)
    def test_invalid_cape(self, mock_put: mock.MagicMock):
        self.assertRaises(
            NotCapeOwner,
            session.show_user_cape,
            VALID_ACCESS_TOKEN,
            INVALID_CAPE_ID,
        )
