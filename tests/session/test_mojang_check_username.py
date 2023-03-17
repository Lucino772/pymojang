import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_check_username
from mojang.exceptions import Unauthorized


class TestMojangCheckUsername(unittest.TestCase):
    @responses.activate
    def test_available(self):
        name = "lucino"
        responses.add(
            method=responses.GET,
            url=api_session_check_username(name),
            json={"status": "AVAILABLE"},
            status=200,
        )

        available = session.check_username("TOKEN", name)
        self.assertTrue(available)

    @responses.activate
    def test_unavailable(self):
        name = "lucino"
        responses.add(
            method=responses.GET,
            url=api_session_check_username(name),
            json={"status": "DUPLICATE"},
            status=200,
        )

        available = session.check_username("TOKEN", name)
        self.assertFalse(available)

    @responses.activate
    def test401(self):
        name = "lucino"
        responses.add(
            method=responses.GET,
            url=api_session_check_username(name),
            status=401,
        )

        self.assertRaises(Unauthorized, session.check_username, "TOKEN", name)

    @responses.activate
    def test429(self):
        name = "lucino"
        responses.add(
            method=responses.GET,
            url=api_session_check_username(name),
            status=429,
        )

        self.assertRaises(RuntimeError, session.check_username, "TOKEN", name)
