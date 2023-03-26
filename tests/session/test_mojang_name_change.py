import datetime as dt
import unittest

import responses

from mojang.api import session
from mojang.api.urls import api_session_name_change
from mojang.exceptions import Unauthorized


class TestMojangNameChange(unittest.TestCase):
    @responses.activate
    def test200(self):
        date = dt.datetime.utcnow()
        responses.add(
            method=responses.GET,
            url=api_session_name_change,
            json={
                "createdAt": date.isoformat(sep="T").replace("+00:00", "Z"),
                "nameChangeAllowed": True,
            },
            status=200,
        )

        ret = session.get_user_name_change("TOKEN")
        self.assertTrue(ret.allowed)
        self.assertEqual(
            ret.created_at,
            date,
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
