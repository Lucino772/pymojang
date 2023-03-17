import datetime as dt
import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_name_change
from mojang.exceptions import Unauthorized


class TestMojangNameChange(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(
            method=responses.GET,
            url=api_session_name_change,
            json={
                "createdAt": "2021-01-01T00:00:00Z",
                "nameChangeAllowed": True,
            },
            status=200,
        )

        ret = session.get_user_name_change("TOKEN")
        self.assertTrue(ret.allowed)
        self.assertEqual(
            ret.created_at,
            dt.datetime.strptime("2021-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        )

    @responses.activate
    def test400(self):
        responses.add(
            method=responses.GET, url=api_session_name_change, status=400
        )

        self.assertRaises(ValueError, session.get_user_name_change, "TOKEN")

    @responses.activate
    def test401(self):
        responses.add(
            method=responses.GET, url=api_session_name_change, status=401
        )

        self.assertRaises(Unauthorized, session.get_user_name_change, "TOKEN")
