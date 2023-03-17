import os
import unittest
from contextlib import contextmanager

import responses

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
        self.dirname = os.path.dirname(__file__)
        self.assets = os.path.join(self.dirname, "assets")
        self.skin_path = os.path.join(self.assets, "skin.png")
        with open(self.skin_path, "rb") as fp:
            self.skin_data = fp.read()

    def _patch_skin_url(self, url: str, content_type: str = None):
        responses.add(
            method=responses.GET,
            url=url,
            body=self.skin_data,
            status=200,
            content_type=content_type,
        )

    @responses.activate
    def test_autoload_url(self):
        url = "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b"
        self._patch_skin_url(url, "image/png")

        resource = _Resource(source=url, load=True)

        self.assertEqual(resource.extension, "png")
        self.assertEqual(resource.data, self.skin_data)

    def test_autoload_local(self):
        resource = _Resource(source=self.skin_path, load=True)
        self.assertEqual(resource.extension, "png")
        self.assertEqual(resource.data, self.skin_data)

    @responses.activate
    def test_lazyload_url(self):
        url = "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b"
        self._patch_skin_url(url, "image/png")

        resource = _Resource(source=url, load=False)
        resource.load()

        self.assertEqual(resource.extension, "png")
        self.assertEqual(resource.data, self.skin_data)

    def test_lazyload_local(self):
        resource = _Resource(source=self.skin_path, load=False)
        resource.load()

        self.assertEqual(resource.extension, "png")
        self.assertEqual(resource.data, self.skin_data)

    @responses.activate
    def test_filename_from_url(self):
        url = "https://pngset.com/images/best-36-minecraft-skins-boy-hd-wallpapers-skin-minecraft-pe-cute-boy-bottle-beverage-drink-costume-transparent-png-780399.png"
        self._patch_skin_url(url)

        resource = _Resource(source=url, load=True)
        self.assertEqual(resource.extension, "png")
        self.assertEqual(resource.data, self.skin_data)

    def test_save(self):
        resource = _Resource(source=self.skin_path, load=True)

        filename = os.path.join(self.assets, "test_save_skin.png")
        with ensure_deleted(filename):
            resource.save(os.path.join(self.assets, "test_save_skin"), True)

            with open(filename, "rb") as fp:
                content = fp.read()

            self.assertTrue(os.path.exists(filename))
            self.assertEqual(self.skin_data, content)
