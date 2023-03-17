import unittest

import responses

import mojang
from mojang.api.urls import api_get_uuids
from mojang.exceptions import (
    InvalidName,
    MethodNotAllowed,
    NotFound,
    ServerError,
)


class TestMojangStatus(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(
            method=responses.POST,
            url=api_get_uuids,
            json=[
                {"id": "45f50155c09f4fdcb5cee30af2ebd1f0", "name": "_jeb"},
                {"id": "069a79f444e94726a5befca90e38aaf5", "name": "Notch"},
            ],
            status=200,
        )
        usernames1 = ["Notch", "_jeb"]
        uuids1 = mojang.get_uuids(usernames1)
        self.assertDictEqual(
            uuids1,
            {
                "notch": "069a79f444e94726a5befca90e38aaf5",
                "_jeb": "45f50155c09f4fdcb5cee30af2ebd1f0",
            },
        )

        usernames2 = ["_jeb", "Notch"]
        uuids2 = mojang.get_uuids(usernames2)
        self.assertDictEqual(
            uuids2,
            {
                "_jeb": "45f50155c09f4fdcb5cee30af2ebd1f0",
                "notch": "069a79f444e94726a5befca90e38aaf5",
            },
        )

    @responses.activate
    def test204(self):
        responses.add(
            method=responses.POST,
            url=api_get_uuids,
            json=[{"id": "45f50155c09f4fdcb5cee30af2ebd1f0", "name": "_jeb"}],
            status=200,
        )

        uuids = mojang.get_uuids(["_jeb", "UNEXISTENTPLAYER"])
        self.assertDictEqual(
            uuids,
            {
                "_jeb": "45f50155c09f4fdcb5cee30af2ebd1f0",
                "unexistentplayer": None,
            },
        )

    @responses.activate
    def test400(self):
        responses.add(method=responses.POST, url=api_get_uuids, status=400)
        self.assertRaises(
            InvalidName, mojang.get_uuids, ["", "xxxxxxxxxxxxxxxxx"]
        )

    @responses.activate
    def test404(self):
        responses.add(method=responses.POST, url=api_get_uuids, status=404)
        self.assertRaises(NotFound, mojang.get_uuids, ["Notch", "_jeb"])

    @responses.activate
    def test405(self):
        responses.add(method=responses.POST, url=api_get_uuids, status=405)
        self.assertRaises(
            MethodNotAllowed, mojang.get_uuids, ["Notch", "_jeb"]
        )

    @responses.activate
    def test500(self):
        responses.add(method=responses.POST, url=api_get_uuids, status=500)
        self.assertRaises(ServerError, mojang.get_uuids, ["Notch", "_jeb"])
