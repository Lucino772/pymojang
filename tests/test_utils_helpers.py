import unittest

from mojang.api import helpers


class TestUtilsHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.headers1 = helpers.get_headers(json_content=True)
        self.headers2 = helpers.get_headers(bearer="mytoken")

    def test_get_headers_json(self):
        assert self.headers1 == {
            "content-type": "application/json",
            "accept": "application/json",
        }

    def test_get_headers_token(self):
        assert self.headers2 == {"authorization": "Bearer mytoken"}
