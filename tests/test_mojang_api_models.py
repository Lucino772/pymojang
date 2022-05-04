import os
import unittest
from contextlib import contextmanager

from mojang.api.models import Cape, Skin, _Resource


@contextmanager
def ensure_deleted(filename: str):
    try:
        yield
    finally:
        if os.path.exists(filename):
            os.remove(filename)


class TestMojangAPIModels(unittest.TestCase):
    def setUp(self) -> None:
        self.__dirname = os.path.dirname(__file__)
        self.__assets = os.path.join(self.__dirname, "assets")

    def test_autoload_url(self):
        resource = _Resource(
            source="http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
            load=True,
        )
        self.assertEqual(resource.extension, "png")

    def test_autoload_local(self):
        resource = _Resource(
            source=os.path.join(self.__assets, "skin.png"), load=True
        )
        self.assertEqual(resource.extension, "png")

    def test_filename_from_url(self):
        resource = _Resource(
            source="https://pngset.com/images/best-36-minecraft-skins-boy-hd-wallpapers-skin-minecraft-pe-cute-boy-bottle-beverage-drink-costume-transparent-png-780399.png",
            load=True,
        )
        self.assertEqual(resource.extension, "png")

    def test_save(self):
        resource = _Resource(
            source=os.path.join(self.__assets, "skin.png"), load=True
        )
        with ensure_deleted(os.path.join(self.__assets, "test_save_skin.png")):
            resource.save(os.path.join(self.__assets, "test_save_skin"), True)
