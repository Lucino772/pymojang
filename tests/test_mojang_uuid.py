import unittest

import mojang
from mojang.exceptions import InvalidName


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.notch = mojang.get_uuid("Notch")
        self.jeb_ = mojang.get_uuid("jeb_")
        self.unkown = mojang.get_uuid("UNEXISTENTPLAYER")

    def test_existent_uuid(self):
        self.assertEqual(self.notch, "069a79f444e94726a5befca90e38aaf5")
        self.assertEqual(self.jeb_, "853c80ef3c3749fdaa49938b674adae6")

    def test_unexistent_uuid(self):
        self.assertEqual(self.unkown, None)

    def test_invalid_uuid(self):
        self.assertRaises(InvalidName, mojang.get_uuid, "")
        self.assertRaises(InvalidName, mojang.get_uuid, "xxxxxxxxxxxxxxxxx")
