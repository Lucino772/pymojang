import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_change_name
from mojang.exceptions import InvalidName, Unauthorized, UnavailableName


class TestMojangChangeName(unittest.TestCase):
    @responses.activate
    def test200(self):
        name = "lucino"
        responses.add(
            method=responses.PUT, url=api_session_change_name(name), status=200
        )
        changed = session.change_user_name("TOKEN", name)
        self.assertTrue(changed)

    @responses.activate
    def test400(self):
        name = "lucino"
        responses.add(
            method=responses.PUT, url=api_session_change_name(name), status=400
        )

        self.assertRaises(InvalidName, session.change_user_name, "TOKEN", name)

    @responses.activate
    def test403(self):
        name = "lucino"
        responses.add(
            method=responses.PUT, url=api_session_change_name(name), status=403
        )

        self.assertRaises(
            UnavailableName, session.change_user_name, "TOKEN", name
        )

    @responses.activate
    def test401(self):
        name = "lucino"
        responses.add(
            method=responses.PUT, url=api_session_change_name(name), status=401
        )

        self.assertRaises(
            Unauthorized, session.change_user_name, "TOKEN", name
        )
