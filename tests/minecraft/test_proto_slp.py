import unittest

from mojang.minecraft import slp


class TestProtoSLP(unittest.TestCase):
    def test_known_server(self):
        ping_res = slp.ping(("mc.hypixel.net", 25565))
        self.assertIsNotNone(ping_res)

    def test_unknown_server(self):
        ping_res = slp.ping(("localhost", 25565))
        self.assertIsNone(ping_res)
