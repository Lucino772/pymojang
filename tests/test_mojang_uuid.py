import unittest

import responses

import mojang
from mojang.api.urls import api_get_uuid
from mojang.exceptions import (
    InvalidName,
    MethodNotAllowed,
    NotFound,
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
        self.assertEqual(uuid, "069a79f444e94726a5befca90e38aaf5")

    @responses.activate
    def test204(self):
        username = "UNEXISTENTPLAYER"
        responses.add(
            method=responses.GET, url=api_get_uuid(username), status=204
        )

        uuid = mojang.get_uuid(username)
        self.assertIsNone(uuid)

    @responses.activate
    def test400(self):
        username1 = "xxxxxxxxxxxxxxxxx"
        responses.add(
            method=responses.GET, url=api_get_uuid(username1), status=400
        )

        username2 = ""
        responses.add(
            method=responses.GET, url=api_get_uuid(username2), status=400
        )

        self.assertRaises(InvalidName, mojang.get_uuid, username1)
        self.assertRaises(InvalidName, mojang.get_uuid, username2)

    @responses.activate
    def test404(self):
        username = "UNEXISTENTPLAYER"
        responses.add(
            method=responses.GET, url=api_get_uuid(username), status=404
        )

        uuid = mojang.get_uuid(username)
        self.assertIsNone(uuid)

    @responses.activate
    def test405(self):
        username = "UNEXISTENTPLAYER"
        responses.add(
            method=responses.GET, url=api_get_uuid(username), status=405
        )

        self.assertRaises(MethodNotAllowed, mojang.get_uuid, username)

    @responses.activate
    def test500(self):
        username = "UNEXISTENTPLAYER"
        responses.add(
            method=responses.GET, url=api_get_uuid(username), status=500
        )

        self.assertRaises(ServerError, mojang.get_uuid, username)
