import unittest

import pytest
import responses

import mojang
from mojang.api.urls import api_get_uuid
from mojang.exceptions import (
    InvalidName,
    MethodNotAllowed,
    ServerError,
)


class TestMojangStatus(unittest.TestCase):
    @responses.activate
    def test200(self):
        username = "Notch"
        responses.add(
            method=responses.GET,
            url=api_get_uuid(username),
            json={"id": "069a79f444e94726a5befca90e38aaf5", "name": username},
            status=200,
        )

        uuid = mojang.get_uuid(username)
        assert uuid == "069a79f444e94726a5befca90e38aaf5"

    @responses.activate
    def test204(self):
        username = "UNEXISTENTPLAYER"
        responses.add(method=responses.GET, url=api_get_uuid(username), status=204)

        uuid = mojang.get_uuid(username)
        assert uuid is None

    @responses.activate
    def test400(self):
        username1 = "xxxxxxxxxxxxxxxxx"
        responses.add(method=responses.GET, url=api_get_uuid(username1), status=400)

        username2 = ""
        responses.add(method=responses.GET, url=api_get_uuid(username2), status=400)

        pytest.raises(InvalidName, mojang.get_uuid, username1)
        pytest.raises(InvalidName, mojang.get_uuid, username2)

    @responses.activate
    def test404(self):
        username = "UNEXISTENTPLAYER"
        responses.add(method=responses.GET, url=api_get_uuid(username), status=404)

        uuid = mojang.get_uuid(username)
        assert uuid is None

    @responses.activate
    def test405(self):
        username = "UNEXISTENTPLAYER"
        responses.add(method=responses.GET, url=api_get_uuid(username), status=405)

        pytest.raises(MethodNotAllowed, mojang.get_uuid, username)

    @responses.activate
    def test500(self):
        username = "UNEXISTENTPLAYER"
        responses.add(method=responses.GET, url=api_get_uuid(username), status=500)

        pytest.raises(ServerError, mojang.get_uuid, username)
