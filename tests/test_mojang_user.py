import unittest

import responses

import mojang
from mojang.api.urls import api_user_profile
from mojang.exceptions import MethodNotAllowed, NotFound, ServerError


class TestMojangStatus(unittest.TestCase):
    @responses.activate
    def test200(self):
        # TODO: Test With & Without Cape
        uuid = "069a79f444e94726a5befca90e38aaf5"  # Notch
        responses.add(
            method=responses.GET,
            url=api_user_profile(uuid),
            json={
                "id": uuid,
                "name": "Notch",
                "properties": [
                    {
                        "name": "textures",
                        "value": (
                            "ewogICJ0aW1lc3RhbXAiIDogMTY3ODk2NDQ0MzQ4NSw"
                            "KICAicHJvZmlsZUlkIiA6ICIwNjlhNzlmNDQ0ZTk0Nz"
                            "I2YTViZWZjYTkwZTM4YWFmNSIsCiAgInByb2ZpbGVOY"
                            "W1lIiA6ICJOb3RjaCIsCiAgInRleHR1cmVzIiA6IHsK"
                            "ICAgICJTS0lOIiA6IHsKICAgICAgInVybCIgOiAiaHR"
                            "0cDovL3RleHR1cmVzLm1pbmVjcmFmdC5uZXQvdGV4dH"
                            "VyZS8yOTIwMDlhNDkyNWI1OGYwMmM3N2RhZGMzZWNlZ"
                            "jA3ZWE0Yzc0NzJmNjRlMGZkYzMyY2U1NTIyNDg5MzYy"
                            "NjgwIgogICAgfQogIH0KfQ=="
                        ),
                    }
                ],
            },
            status=200,
        )
        responses.add(
            method=responses.GET,
            url="http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680",
            body=b"",
            status=200,
        )

        profile = mojang.get_profile(uuid)
        self.assertEqual(profile.name, "Notch")
        self.assertEqual(profile.uuid, uuid)
        self.assertEqual(profile.is_legacy, False)
        self.assertEqual(profile.is_demo, False)
        self.assertIsNotNone(profile.skin)
        self.assertEqual(
            profile.skin.source,
            "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680",
        )
        self.assertEqual(profile.skin.variant, "classic")
        self.assertIsNone(profile.cape)

    @responses.activate
    def test204(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(
            method=responses.GET, url=api_user_profile(uuid), status=204
        )

        profile = mojang.get_profile(uuid)
        self.assertIsNone(profile)

    @responses.activate
    def test400(self):
        uuid = "thisisnotauuid"
        responses.add(
            method=responses.GET, url=api_user_profile(uuid), status=400
        )

        self.assertRaises(ValueError, mojang.get_profile, uuid)

    @responses.activate
    def test404(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(
            method=responses.GET, url=api_user_profile(uuid), status=404
        )

        self.assertRaises(NotFound, mojang.get_profile, uuid)

    @responses.activate
    def test405(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(
            method=responses.GET, url=api_user_profile(uuid), status=405
        )

        self.assertRaises(MethodNotAllowed, mojang.get_profile, uuid)

    @responses.activate
    def test500(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(
            method=responses.GET, url=api_user_profile(uuid), status=500
        )

        self.assertRaises(ServerError, mojang.get_profile, uuid)
