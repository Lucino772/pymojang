import unittest

import responses

import mojang
from mojang.api.urls import api_get_blocked_servers
from mojang.exceptions import MethodNotAllowed, NotFound, ServerError

SERVER_HASHES = [
    "0c57a571f5f3b8951abb7d3447daa927731ff367",
    "f5c92f3b5634f32b40b37865ae854e35d3c5cae6",
    "175f82a1dd5d30c160ce8566a8e2fd750e540a4d",
    "b707b4d3011b980a13606b99663cd049d328205a",
    "3f2fe952ebb7e2311854cf5ef49f429bc6b054a2",
    "d1001806c54e32688aaab23ea65598719f3b2f24",
    "5d2e2ad9c13d8d767ca3b34d644c5bb98aab31ff",
    "828237257dac2204ffa578dac31620c3f95cce50",
    "62d497134b1f305513b0cf0571fd7e9718b43559",
    "74ce7de22e615311dcdc019903db18eb71d9602e",
]


class TestMojangBlockedServers(unittest.TestCase):
    @responses.activate
    def test200(self):
        responses.add(
            method=responses.GET,
            url=api_get_blocked_servers,
            body="\n".join(SERVER_HASHES),
            status=200,
        )
        hashes = mojang.get_blocked_servers()
        self.assertListEqual(SERVER_HASHES, hashes)

    @responses.activate
    def test404(self):
        responses.add(
            method=responses.GET, url=api_get_blocked_servers, status=404
        )

        self.assertRaises(NotFound, mojang.get_blocked_servers)

    @responses.activate
    def test405(self):
        responses.add(
            method=responses.GET, url=api_get_blocked_servers, status=405
        )

        self.assertRaises(MethodNotAllowed, mojang.get_blocked_servers)

    @responses.activate
    def test500(self):
        responses.add(
            method=responses.GET, url=api_get_blocked_servers, status=500
        )

        self.assertRaises(ServerError, mojang.get_blocked_servers)
