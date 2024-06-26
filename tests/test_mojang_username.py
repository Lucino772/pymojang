import unittest

import pytest
import responses

import mojang
from mojang.api.urls import api_get_username
from mojang.exceptions import MethodNotAllowed, ServerError


class TestMojangUsername(unittest.TestCase):
    @responses.activate
    def test200(self):
        uuid = "069a79f444e94726a5befca90e38aaf5"
        responses.add(
            method=responses.GET,
            url=api_get_username(uuid),
            json={"id": uuid, "name": "Notch"},
            status=200,
        )

        username = mojang.get_username(uuid)
        assert username == "Notch"

    @responses.activate
    def test204(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_get_username(uuid), status=204)

        username = mojang.get_username(uuid)
        assert username is None

    @responses.activate
    def test400(self):
        uuid = "thisisnotauuid"
        responses.add(method=responses.GET, url=api_get_username(uuid), status=400)

        pytest.raises(ValueError, mojang.get_username, uuid)  # noqa: PT011

    @responses.activate
    def test404(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_get_username(uuid), status=404)

        username = mojang.get_username(uuid)
        assert username is None

    @responses.activate
    def test405(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_get_username(uuid), status=405)

        pytest.raises(MethodNotAllowed, mojang.get_username, uuid)

    @responses.activate
    def test500(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_get_username(uuid), status=500)

        pytest.raises(ServerError, mojang.get_username, uuid)
