import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_product_voucher
from mojang.exceptions import Unauthorized


class TestMojangCheckProductVoucher(unittest.TestCase):
    @responses.activate
    def test200(self):
        voucher = "12345"
        responses.add(
            method=responses.GET,
            url=api_session_product_voucher(voucher),
            status=200,
            json={
                "voucherInfo": {
                    "code": "00000-00000-00000-00000-00000",
                    "productVariant": "minecraft",
                    "status": "ACTIVE",
                },
                "productRedeemable": True,
            },
        )

        available = session.check_product_voucher("TOKEN", voucher)
        self.assertTrue(available)

    @responses.activate
    def test401(self):
        voucher = "12345"
        responses.add(
            method=responses.GET,
            url=api_session_product_voucher(voucher),
            status=401,
        )

        self.assertRaises(
            Unauthorized, session.check_product_voucher, "TOKEN", voucher
        )

    @responses.activate
    def test404_invalid(self):
        voucher = "12345"
        responses.add(
            method=responses.GET,
            url=api_session_product_voucher(voucher),
            status=404,
            json={
                "path": "/productvoucher/:voucher",
                "errorType": "NOT_FOUND",
                "error": "NOT_FOUND",
            },
        )

        self.assertRaises(
            ValueError, session.check_product_voucher, "TOKEN", voucher
        )

    @responses.activate
    def test404_unavailable(self):
        voucher = "12345"
        responses.add(
            method=responses.GET,
            url=api_session_product_voucher(voucher),
            status=404,
            json={
                "path": "/productvoucher/:voucher",
                "errorType": "NOT_FOUND",
                "error": "NOT_FOUND",
                "errorMessage": "The server has not found anything matching the request URI",
                "developerMessage": "The server has not found anything matching the request URI",
            },
        )

        available = session.check_product_voucher("TOKEN", voucher)
        self.assertFalse(available)


class TestMojangRedeemProductVoucher(unittest.TestCase):
    @responses.activate
    def test200(self):
        voucher = "12345"
        responses.add(
            method=responses.PUT,
            url=api_session_product_voucher(voucher),
            status=200,
            json={
                "voucherInfo": {
                    "code": "00000-00000-00000-00000-00000",
                    "productVariant": "minecraft",
                    "status": "ACTIVE",
                },
                "productRedeemable": True,
            },
        )

        available = session.redeem_product_voucher("TOKEN", voucher)
        self.assertTrue(available)

    @responses.activate
    def test401(self):
        voucher = "12345"
        responses.add(
            method=responses.PUT,
            url=api_session_product_voucher(voucher),
            status=401,
        )

        self.assertRaises(
            Unauthorized, session.redeem_product_voucher, "TOKEN", voucher
        )

    @responses.activate
    def test404_invalid(self):
        voucher = "12345"
        responses.add(
            method=responses.PUT,
            url=api_session_product_voucher(voucher),
            status=404,
            json={
                "path": "/productvoucher/:voucher",
                "errorType": "NOT_FOUND",
                "error": "NOT_FOUND",
            },
        )

        self.assertRaises(
            ValueError, session.redeem_product_voucher, "TOKEN", voucher
        )

    @responses.activate
    def test404_unavailable(self):
        voucher = "12345"
        responses.add(
            method=responses.PUT,
            url=api_session_product_voucher(voucher),
            status=404,
            json={
                "path": "/productvoucher/:voucher",
                "errorType": "NOT_FOUND",
                "error": "NOT_FOUND",
                "errorMessage": "The server has not found anything matching the request URI",
                "developerMessage": "The server has not found anything matching the request URI",
            },
        )

        available = session.redeem_product_voucher("TOKEN", voucher)
        self.assertFalse(available)
