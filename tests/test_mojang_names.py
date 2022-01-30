import unittest

import mojang
from mojang.api.structures.base import NameInfo, NameInfoList
from mojang.exceptions import InvalidName


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.notch = mojang.names("069a79f444e94726a5befca90e38aaf5")
        self.jeb_ = mojang.names("853c80ef3c3749fdaa49938b674adae6")

        self.unkown = mojang.names("069a79f444e94726a5befca90e38aaf6")

    def test_existent_names(self):
        self.assertEqual(self.notch, NameInfoList([NameInfo("Notch", None)]))
        self.assertEqual(self.jeb_, NameInfoList([NameInfo("jeb_", None)]))

    def test_unexistent_names(self):
        self.assertEqual(self.unkown, None)

    def test_invalid_names(self):
        self.assertRaises(ValueError, mojang.names, "thisisnotauuid")
