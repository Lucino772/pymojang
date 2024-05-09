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
        assert len(self._versions) > 0
        assert self._latest_rel is not None
        assert self._latest_snap is not None

    def test_get_latest_version_release(self):
        version = minecraft.get_version(version="latest", snapshot=False)
        assert version.id == self._latest_rel

    def test_get_latest_version_snapshot(self):
        version = minecraft.get_version(version="latest", snapshot=True)
        assert version.id == self._latest_snap

    def test_get_random_version(self):
        version = minecraft.get_version(version="1.12.1")
        assert version.id == "1.12.1"

    def test_get_unknown_version(self):
        version = minecraft.get_version(version="NOT_A_VERSION")
        assert version is None
