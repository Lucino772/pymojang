import unittest

import pytest
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
        assert profile.name == "Notch"
        assert profile.uuid == uuid
        assert profile.is_legacy == False
        assert profile.is_demo == False
        assert profile.skin is not None
        assert (
            profile.skin.source
            == "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680"
        )
        assert profile.skin.variant == "classic"
        assert profile.cape is None

    @responses.activate
    def test204(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_user_profile(uuid), status=204)

        profile = mojang.get_profile(uuid)
        assert profile is None

    @responses.activate
    def test400(self):
        uuid = "thisisnotauuid"
        responses.add(method=responses.GET, url=api_user_profile(uuid), status=400)

        pytest.raises(ValueError, mojang.get_profile, uuid)  # noqa: PT011

    @responses.activate
    def test404(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_user_profile(uuid), status=404)

        pytest.raises(NotFound, mojang.get_profile, uuid)

    @responses.activate
    def test405(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_user_profile(uuid), status=405)

        pytest.raises(MethodNotAllowed, mojang.get_profile, uuid)

    @responses.activate
    def test500(self):
        uuid = "069a79f444e94726a5befca90e38aaf6"  # Does not exists
        responses.add(method=responses.GET, url=api_user_profile(uuid), status=500)

        pytest.raises(ServerError, mojang.get_profile, uuid)
