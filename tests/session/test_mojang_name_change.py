import datetime as dt
import unittest

import pytest
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
        assert ret.allowed
        assert ret.created_at == date

    @responses.activate
    def test400(self):
        responses.add(method=responses.GET, url=api_session_name_change, status=400)

        pytest.raises(ValueError, session.get_user_name_change, "TOKEN")  # noqa: PT011

    @responses.activate
    def test401(self):
        responses.add(method=responses.GET, url=api_session_name_change, status=401)

        pytest.raises(Unauthorized, session.get_user_name_change, "TOKEN")
