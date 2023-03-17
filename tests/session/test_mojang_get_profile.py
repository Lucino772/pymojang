import unittest

import responses

from mojang.api import session
from mojang.api.models import Cape, Skin
from mojang.api.urls import api_session_profile
from mojang.exceptions import Unauthorized


class TestMojangGetProfile(unittest.TestCase):
    def _patch_skin_url(self, url: str):
        responses.add(method=responses.GET, url=url, body=b"", status=200)

    @responses.activate
    def test200(self):
        self._patch_skin_url(
            "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b"
        )
        responses.add(
            method=responses.GET,
            url=api_session_profile,
            json={
                "id": "4ba22ce11f064d7f9f715634aa0d7973",
                "name": "Lucino772",
                "skins": [
                    {
                        "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                        "state": "ACTIVE",
                        "url": "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                        "variant": "CLASSIC",
                        "alias": "STEVE",
                    }
                ],
                "capes": [
                    {
                        "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                        "state": "ACTIVE",
                        "url": "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                    }
                ],
            },
            status=200,
        )

        profile = session.get_profile("TOKEN")
        self.assertEqual(profile.uuid, "4ba22ce11f064d7f9f715634aa0d7973")
        self.assertEqual(profile.name, "Lucino772")
        self.assertEqual(
            profile.skins,
            [
                Skin(
                    "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                    "CLASSIC",
                    "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "ACTIVE",
                )
            ],
        )
        self.assertEqual(
            profile.capes,
            [
                Cape(
                    "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                    "6a6e65e5-76dd-4c3c-a625-162924514568",
                    "ACTIVE",
                )
            ],
        )

    @responses.activate
    def test401(self):
        responses.add(
            method=responses.GET, url=api_session_profile, status=401
        )

        self.assertRaises(Unauthorized, session.get_profile, "TOKEN")
