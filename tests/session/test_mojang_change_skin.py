import unittest

import responses
from responses.matchers import multipart_matcher

from mojang.api import session
from mojang.api.models import Skin
from mojang.api.urls import api_session_change_skin
from mojang.exceptions import Unauthorized


class TestMojangChangeSkin(unittest.TestCase):
    def _path_skin_url(self, url: str):
        responses.add(method=responses.GET, url=url, status=200, body=b"")

    @responses.activate
    def test204(self):
        skin_url = "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680"
        self._path_skin_url(skin_url)
        skin = Skin(source=skin_url, variant="classic")

        responses.add(
            method=responses.POST,
            url=api_session_change_skin,
            status=204,
            match=[
                multipart_matcher(
                    {"file": ("image.png", skin.data, "image/png")},
                    data={"variant": "classic"},
                )
            ],
        )

        changed = session.change_user_skin("TOKEN", skin_url)
        self.assertTrue(changed)

    @responses.activate
    def test400(self):
        skin_url = "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680"
        self._path_skin_url(skin_url)
        responses.add(
            method=responses.POST, url=api_session_change_skin, status=400
        )

        self.assertRaises(
            ValueError, session.change_user_skin, "TOKEN", skin_url
        )

    @responses.activate
    def test401(self):
        skin_url = "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680"
        self._path_skin_url(skin_url)
        responses.add(
            method=responses.POST, url=api_session_change_skin, status=401
        )

        self.assertRaises(
            Unauthorized, session.change_user_skin, "TOKEN", skin_url
        )
