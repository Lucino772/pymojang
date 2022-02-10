import unittest

import mojang


class TestMojangBlockedServers(unittest.TestCase):
    def test(self):
        self.assertGreater(len(mojang.get_blocked_servers()), 0)
