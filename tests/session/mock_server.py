import json
from urllib.parse import urlparse

import jwt
from requests.models import Response


class MockSessionServer:
    def __init__(
        self,
        access_token: str,
        unavailable_names: list = [],
        valid_cape_ids=[],
        valid_vouchers=[],
        used_vouchers=[],
        game_private_key: str = None,
        game_public_key: str = None,
    ) -> None:
        self._access_token = access_token
        self._unavailable_names = unavailable_names
        self._valid_cape_ids = valid_cape_ids
        self._valid_vouchers = valid_vouchers
        self._used_vouchers = used_vouchers
        self._game_private_key = game_private_key
        self._game_public_key = game_public_key

    def _is_token_valid(self, headers: dict):
        authorization = headers.get("authorization", None)
        if authorization is None:
            return False

        token = str(authorization).split(" ")[1]
        return token == self._access_token

    def product_voucher(self, url, **kwargs):
        voucher = urlparse(url).path.split("/")[-1]
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        elif voucher not in self._valid_vouchers:
            response.status_code = 404
            response._content = json.dumps(
                {
                    "path": "/productvoucher/:voucher",
                    "errorType": "NOT_FOUND",
                    "error": "NOT_FOUND",
                }
            ).encode("utf-8")
            response.encoding = "utf-8"
        elif voucher in self._used_vouchers:
            response.status_code = 404
            response._content = json.dumps(
                {
                    "path": "/productvoucher/:voucher",
                    "errorType": "NOT_FOUND",
                    "error": "NOT_FOUND",
                    "errorMessage": "The server has not found anything matching the request URI",
                    "developerMessage": "The server has not found anything matching the request URI",
                }
            ).encode("utf-8")
            response.encoding = "utf-8"
        else:
            response.status_code = 200
            response._content = json.dumps(
                {
                    "voucherInfo": {
                        "code": "00000-00000-00000-00000-00000",
                        "productVariant": "minecraft",
                        "status": "ACTIVE",
                    },
                    "productRedeemable": True,
                }
            ).encode("utf-8")
            response.encoding = "utf-8"

        return response

    def check_username(self, url, *args, **kwargs):
        username = urlparse(url).path.split("/")[-2]
        response = Response()
        if not self._is_token_valid(kwargs.get("headers", {})):
            response.status_code = 401
        elif username in self._unavailable_names:
            response.status_code = 200
            response._content = json.dumps({"status": "DUPLICATE"}).encode(
                "utf-8"
            )
            response.encoding = "utf-8"
        else:
            response.status_code = 200
            response._content = json.dumps({"status": "AVAILABLE"}).encode(
                "utf-8"
            )
            response.encoding = "utf-8"

        return response

    def check_username_429(self, url, *args, **kwargs):
        response = self.check_username(url, *args, **kwargs)
        response.status_code = 429
        response._content = json.dumps(
            {
                "path": "/minecraft/profile/name/:username/available",
                "errorType": "TooManyRequestsException",
                "error": "TooManyRequestsException",
                "errorMessage": "The client has sent too many requests within a certain amount of time",
                "developerMessage": "The client has sent too many requests within a certain amount of time",
            }
        ).encode("utf-8")
        return response

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
            product_minecraft_sig = jwt.encode(
                {"signerId": "2535416586892404", "name": "product_minecraft"},
                self._game_private_key,
                algorithm="RS256",
            )
            game_minecraft_sig = jwt.encode(
                {"signerId": "2535416586892404", "name": "game_minecraft"},
                self._game_private_key,
                algorithm="RS256",
            )
            signature = jwt.encode(
                {
                    "entitlements": [
                        {"name": "product_minecraft"},
                        {"name": "game_minecraft"},
                    ],
                    "signerId": "2535416586892404",
                },
                self._game_private_key,
                algorithm="RS256",
            )

            response.status_code = 200
            response._content = json.dumps(
                {
                    "items": [
                        {
                            "name": "product_minecraft",
                            "signature": product_minecraft_sig,
                        },
                        {
                            "name": "game_minecraft",
                            "signature": game_minecraft_sig,
                        },
                    ],
                    "signature": signature,
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
                    "capes": [
                        {
                            "id": "6a6e65e5-76dd-4c3c-a625-162924514568",
                            "state": "ACTIVE",
                            "url": "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                        }
                    ],
                }
            ).encode("utf-8")
            response.encoding = "utf-8"

        return response
