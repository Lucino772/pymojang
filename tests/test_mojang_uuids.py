import unittest

import mojang
from mojang.api.structures.base import UUIDInfo
from mojang.exceptions import InvalidName


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.order1 = mojang.get_uuids(["Notch", "jeb_"])
        self.order2 = mojang.get_uuids(["jeb_", "Notch"])

        self.unkown1 = mojang.get_uuids(["jeb_", "UNEXISTENTPLAYER"])
        self.unkown2 = mojang.get_uuids(["UNEXISTENTPL1", "UNEXISTENTPL2"])

    def test_existent_uuids(self):
        self.assertEqual(
            self.order1,
            [
                UUIDInfo("Notch", "069a79f444e94726a5befca90e38aaf5"),
                UUIDInfo("jeb_", "853c80ef3c3749fdaa49938b674adae6"),
            ],
        )
        self.assertEqual(
            self.order2,
            [
                UUIDInfo("jeb_", "853c80ef3c3749fdaa49938b674adae6"),
                UUIDInfo("Notch", "069a79f444e94726a5befca90e38aaf5"),
            ],
        )

    def test_unexistent_uuids(self):
        self.assertEqual(
            self.unkown1,
            [UUIDInfo("jeb_", "853c80ef3c3749fdaa49938b674adae6"), None],
        )
        self.assertEqual(self.unkown2, [None, None])

    def test_invalid_uuids(self):
        self.assertRaises(InvalidName, mojang.get_uuids, ["", "jeb_"])
        self.assertRaises(
            InvalidName, mojang.get_uuids, ["jeb_", "xxxxxxxxxxxxxxxxx"]
        )
