import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_cape_visibility
from mojang.exceptions import Unauthorized


class TestMojangHideCape(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(
            method=responses.DELETE,
            url=api_session_cape_visibility,
            status=200,
        )

        hidden = session.hide_user_cape("TOKEN")
        self.assertTrue(hidden)

    @responses.activate
    def test401(self):
        responses.add(
            method=responses.DELETE,
            url=api_session_cape_visibility,
            status=401,
        )

        self.assertRaises(Unauthorized, session.hide_user_cape, "TOKEN")
