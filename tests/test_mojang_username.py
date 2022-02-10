import unittest

import mojang


class TestMojangUsername(unittest.TestCase):
    def setUp(self) -> None:
        self.notch = mojang.get_username("069a79f444e94726a5befca90e38aaf5")
        self.unkown = mojang.get_username("069a79f444e94726a5befca90e38aaf6")

    def test_know_uuid(self):
        self.assertEqual(self.notch, "Notch")

    def test_unkown_uuid(self):
        self.assertEqual(self.unkown, None)

    def test_invalid_uuid(self):
        self.assertRaises(ValueError, mojang.get_username, ["thisisnotauuid"])
