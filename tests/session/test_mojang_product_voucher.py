import datetime as dt
import unittest
from unittest import mock

from mojang.api import session
from mojang.exceptions import Unauthorized

from .mock_server import MockSessionServer

VALID_ACCESS_TOKEN = "MY_ACCESS_TOKEN"
INVALID_ACCESS_TOKEN = "NOT_MY_ACCESS_TOKEN"

mock_server = MockSessionServer(
    VALID_ACCESS_TOKEN,
    valid_vouchers=["8901854197", "JHRD2-HWGTY-WP3MW-QR4MC-CGGHZ"],
    used_vouchers=["JHRD2-HWGTY-WP3MW-QR4MC-CGGHZ"],
)


class TestMojangCheckProductVoucher(unittest.TestCase):
    @mock.patch("requests.get", side_effect=mock_server.product_voucher)
    def test_invalid_voucher(self, mock_get: mock.MagicMock):
        self.assertRaises(
            ValueError,
            session.check_product_voucher,
            VALID_ACCESS_TOKEN,
            "12345",
        )

    @mock.patch("requests.get", side_effect=mock_server.product_voucher)
    def test_used_voucher(self, mock_get: mock.MagicMock):
        res = session.check_product_voucher(
            VALID_ACCESS_TOKEN, "JHRD2-HWGTY-WP3MW-QR4MC-CGGHZ"
        )
        self.assertEqual(res, False)

    @mock.patch("requests.get", side_effect=mock_server.product_voucher)
    def test_unused_voucher(self, mock_get: mock.MagicMock):
        res = session.check_product_voucher(VALID_ACCESS_TOKEN, "8901854197")
        self.assertEqual(res, True)

    @mock.patch("requests.get", side_effect=mock_server.product_voucher)
    def test_invalid_token(self, mock_get: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.check_product_voucher,
            INVALID_ACCESS_TOKEN,
            "8901854197",
        )


class TestMojangRedeemProductVoucher(unittest.TestCase):
    @mock.patch("requests.put", side_effect=mock_server.product_voucher)
    def test_invalid_voucher(self, mock_put: mock.MagicMock):
        self.assertRaises(
            ValueError,
            session.redeem_product_voucher,
            VALID_ACCESS_TOKEN,
            "12345",
        )

    @mock.patch("requests.put", side_effect=mock_server.product_voucher)
    def test_used_voucher(self, mock_put: mock.MagicMock):
        res = session.redeem_product_voucher(
            VALID_ACCESS_TOKEN, "JHRD2-HWGTY-WP3MW-QR4MC-CGGHZ"
        )
        self.assertEqual(res, False)

    @mock.patch("requests.put", side_effect=mock_server.product_voucher)
    def test_unused_voucher(self, mock_put: mock.MagicMock):
        res = session.redeem_product_voucher(VALID_ACCESS_TOKEN, "8901854197")
        self.assertEqual(res, True)

    @mock.patch("requests.put", side_effect=mock_server.product_voucher)
    def test_invalid_token(self, mock_put: mock.MagicMock):
        self.assertRaises(
            Unauthorized,
            session.redeem_product_voucher,
            INVALID_ACCESS_TOKEN,
            "8901854197",
        )
