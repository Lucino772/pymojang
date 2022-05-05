import unittest

from mojang import minecraft


class TestMojangAPIModels(unittest.TestCase):
    def setUp(self) -> None:
        (
            self._versions,
            self._latest_rel,
            self._latest_snap,
        ) = minecraft.get_versions()

    def test_get_versions(self):
        self.assertGreater(len(self._versions), 0)
        self.assertIsNotNone(self._latest_rel)
        self.assertIsNotNone(self._latest_snap)

    def test_get_latest_version_release(self):
        version = minecraft.get_version(version="latest", snapshot=False)
        self.assertEqual(version.id, self._latest_rel)

    def test_get_latest_version_snapshot(self):
        version = minecraft.get_version(version="latest", snapshot=True)
        self.assertEqual(version.id, self._latest_snap)

    def test_get_random_version(self):
        version = minecraft.get_version(version="1.12.1")
        self.assertEqual(version.id, "1.12.1")

    def test_get_unknown_version(self):
        version = minecraft.get_version(version="NOT_A_VERSION")
        self.assertIsNone(version)
