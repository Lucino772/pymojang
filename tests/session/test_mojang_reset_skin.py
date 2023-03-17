import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_reset_skin
from mojang.exceptions import Unauthorized


class TestMojangResetSkin(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(
            method=responses.DELETE, url=api_session_reset_skin, status=200
        )

        reset = session.reset_user_skin("TOKEN")
        self.assertTrue(reset)

    @responses.activate
    def test400(self):
        responses.add(
            method=responses.DELETE, url=api_session_reset_skin, status=400
        )

        self.assertRaises(ValueError, session.reset_user_skin, "TOKEN")

    @responses.activate
    def test401(self):
        responses.add(
            method=responses.DELETE, url=api_session_reset_skin, status=401
        )

        self.assertRaises(Unauthorized, session.reset_user_skin, "TOKEN")
