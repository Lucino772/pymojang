import unittest

import mojang
from mojang.api.base import ServiceStatus


class TestMojangStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.value = mojang.get_status()

    def test_status(self):
        expected = [
            ServiceStatus(name="minecraft.net", status="unknown"),
            ServiceStatus(name="session.minecraft.net", status="unknown"),
            ServiceStatus(name="account.mojang.com", status="unknown"),
            ServiceStatus(name="authserver.mojang.com", status="unknown"),
            ServiceStatus(name="sessionserver.mojang.com", status="unknown"),
            ServiceStatus(name="api.mojang.com", status="unknown"),
            ServiceStatus(name="textures.minecraft.net", status="unknown"),
            ServiceStatus(name="mojang.com", status="unknown"),
        ]

        self.assertListEqual(expected, self.value)
