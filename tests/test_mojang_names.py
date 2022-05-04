import datetime
import unittest

import mojang
from mojang.api.structures import NameInfo


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.notch = mojang.get_names("069a79f444e94726a5befca90e38aaf5")
        self.jeb_ = mojang.get_names("853c80ef3c3749fdaa49938b674adae6")
        self.mumbo = mojang.get_names("ac224782efff4296b08cdbde8e47abdb")

        self.unkown = mojang.get_names("069a79f444e94726a5befca90e38aaf6")

    def test_existent_names(self):
        self.assertListEqual(self.notch, [NameInfo("Notch", None)])
        self.assertListEqual(self.jeb_, [NameInfo("jeb_", None)])
        self.assertListEqual(
            self.mumbo,
            [
                NameInfo(
                    name="Mumbo",
                    changed_to_at=datetime.datetime(2016, 4, 5, 14, 50, 11),
                ),
                NameInfo(
                    name="MedShow",
                    changed_to_at=datetime.datetime(2016, 3, 19, 5, 45, 51),
                ),
                NameInfo(
                    name="Mumbo",
                    changed_to_at=datetime.datetime(2015, 2, 4, 12, 40, 8),
                ),
                NameInfo(name="MrMumbo", changed_to_at=None),
            ],
        )

    def test_unexistent_names(self):
        self.assertListEqual(self.unkown, [])

    def test_invalid_names(self):
        self.assertRaises(ValueError, mojang.get_names, "thisisnotauuid")
