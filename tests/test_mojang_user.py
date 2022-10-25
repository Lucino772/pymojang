import unittest

import mojang
from mojang.api.models import Cape, Skin
from mojang.api.structures import UnauthenticatedProfile
from mojang.exceptions import InvalidName


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.notch = mojang.get_profile("069a79f444e94726a5befca90e38aaf5")
        self.jeb_ = mojang.get_profile("853c80ef3c3749fdaa49938b674adae6")
        self.unkown = mojang.get_profile("069a79f444e94726a5befca90e38aaf6")

    def test_existent_user(self):
        self.assertEqual(
            self.notch,
            UnauthenticatedProfile(
                "Notch",
                "069a79f444e94726a5befca90e38aaf5",
                False,
                False,
                Skin(
                    "http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680",
                    "classic",
                ),
                None,
            ),
        )

        self.assertEqual(
            self.jeb_,
            UnauthenticatedProfile(
                "jeb_",
                "853c80ef3c3749fdaa49938b674adae6",
                False,
                False,
                Skin(
                    "http://textures.minecraft.net/texture/7fd9ba42a7c81eeea22f1524271ae85a8e045ce0af5a6ae16c6406ae917e68b5",
                    "classic",
                ),
                Cape(
                    "http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995d17d0da995662913fb00f7"
                ),
            ),
        )

    def test_unexistent_user(self):
        self.assertEqual(self.unkown, None)

    def test_invalid_user(self):
        self.assertRaises(ValueError, mojang.get_profile, "thisisnotauuid")
