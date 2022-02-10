import unittest

import mojang


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.no_keys = mojang.get_sales()
        self.valid_keys = mojang.get_sales(
            ["item_sold_minecraft", "item_sold_cobalt"]
        )

    def test_valid_keys(self):
        self.assertIsInstance(self.valid_keys, tuple)

    def test_no_keys(self):
        self.assertTupleEqual(self.no_keys, (0, 0, 0))

    def test_invalid_keys(self):
        self.assertRaises(ValueError, mojang.get_sales, ["some_random_key"])
