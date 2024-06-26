import unittest

import pytest
import responses

from mojang.api import session
from mojang.api.urls import api_session_cape_visibility
from mojang.exceptions import NotCapeOwner, Unauthorized


class TestMojangShowCape(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(method=responses.PUT, url=api_session_cape_visibility, status=200)

        visible = session.show_user_cape("TOKEN", "100")
        assert visible

    @responses.activate
    def test400(self):
        responses.add(method=responses.PUT, url=api_session_cape_visibility, status=400)

        pytest.raises(NotCapeOwner, session.show_user_cape, "TOKEN", "100")

    @responses.activate
    def test401(self):
        responses.add(method=responses.PUT, url=api_session_cape_visibility, status=401)

        pytest.raises(Unauthorized, session.show_user_cape, "TOKEN", "100")
