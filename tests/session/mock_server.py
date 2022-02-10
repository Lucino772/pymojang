import json
from urllib.parse import urlparse

from requests.models import Response


class MockSessionServer:
    def __init__(
        self,
        access_token: str,
        unavailable_names: list = [],
        valid_cape_ids=[],
    ) -> None:
        self._access_token = access_token
        self._unavailable_names = unavailable_names
        self._valid_cape_ids = valid_cape_ids

    def _is_token_valid(self, headers: dict):
        authorization = headers.get("authorization", None)
        if authorization is None:
            return False

        token = str(authorization).split(" ")[1]
        return token == self._access_token

    def user_name_change(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 200
            response._content = json.dumps(
                {
                    "createdAt": "2021-01-01T00:00:00Z",
                    "nameChangeAllowed": True,
                }
            ).encode("utf-8")
            response.encoding = "utf-8"

        return response

    def change_user_name(self, url, **kwargs):
        name = urlparse(url).path.split("/")[-1]
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        elif name in self._unavailable_names:
            response.status_code = 403
        elif not (0 < len(name) <= 16):
            response.status_code = 400
        else:
            response.status_code = 200

        return response

    def change_user_skin(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 204

        return response

    def reset_user_skin(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 200

        return response

    def show_user_cape(self, *args, **kwargs):
        response = Response()
        cape_id = kwargs.get("json", {}).get("capeId")
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        elif cape_id not in self._valid_cape_ids:
            response.status_code = 400
        else:
            response.status_code = 200

        return response

    def hide_user_cape(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 200

        return response

    def owns_minecraft(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 200
            response._content = json.dumps(
                {
                    "items": [
                        {"name": "product_minecraft", "signature": None},
                        {"name": "game_minecraft", "signature": None},
                    ],
                    "signature": None,
                    "keyId": "1",
                }
            ).encode("utf-8")
            response.encoding = "utf-8"

        return response

    def get_profile(self, *args, **kwargs):
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        else:
            response.status_code = 200
            response._content = json.dumps(
                {
                    "id": "4ba22ce11f064d7f9f715634aa0d7973",
                    "name": "Lucino772",
                    "skins": [
                        {
                            "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                            "state": "ACTIVE",
                            "url": "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                            "variant": "CLASSIC",
                            "alias": "STEVE",
                        }
                    ],
                    "capes": [],
                }
            ).encode("utf-8")
            response.encoding = "utf-8"

        return response
