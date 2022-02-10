from typing import Tuple

import requests

from mojang.exceptions import (
    Unauthorized,
    XboxLiveAuthenticationError,
    XboxLiveInvalidUserHash,
)

from .. import helpers, urls


def authenticate_xbl(auth_token: str) -> Tuple[str, str]:
    """Authenticate with Xbox Live using the Microsoft access token
    received after the OAuth authentication

    :param str auth_token: The access token

    :returns: A tuple with the Xbox Live token and user hash

    :raises XboxLiveAuthenticationError: if the auth token is invalid
    """
    headers = helpers.get_headers(json_content=True)
    payload = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": "d={}".format(auth_token),
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT",
    }

    response = requests.post(
        urls.api_ms_xbl_authenticate,
        headers=headers,
        json=payload,
    )
    _, data = helpers.err_check(response, (400, XboxLiveAuthenticationError))
    return data["Token"], data["DisplayClaims"]["xui"][0]["uhs"]


def authenticate_xsts(xbl_token: str) -> Tuple[str, str]:
    """Retrieve the XSTS Token using the Xbox Live token

    :params str xbl_token: The Xbox Live token

    :returns: A tuple with the XSTS token and user hash

    :raises XboxLiveAuthenticationError: if xbl is invalid
    """
    headers = helpers.get_headers(json_content=True)
    payload = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }

    response = requests.post(
        urls.api_ms_xbl_authorize, headers=headers, json=payload
    )
    _, data = helpers.err_check(response, (400, XboxLiveAuthenticationError))
    return data["Token"], data["DisplayClaims"]["xui"][0]["uhs"]


def authenticate_minecraft(userhash: str, xsts_token: str) -> str:
    """Retrieve the Minecraft access token loging in using Xbox Live

    :param str userhash: The user hash from Xbox Live
    :param str xsts_token: The XSTS Token from Xbox Live

    :returns: The minecraft token

    :raises XboxLiveInvalidUserHash: if the user hash is invalid
    :raises Unauthorized: if the XSTS token is invalid

    :Example:

    >>> from mojang.account.auth import microsoft
    >>> ACCESS_TOKEN = '....' # Access token from Microsoft
    >>> xbl_token, _ = microsoft.authenticate_xbl(ACCESS_TOKEN)
    >>> xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
    >>> mc_access_token = microsoft.authenticate_minecraft(userhash, xsts_token)
    """
    headers = helpers.get_headers(json_content=True)
    payload = {"identityToken": f"XBL3.0 x={userhash};{xsts_token}"}

    response = requests.post(
        urls.api_ms_xbl_login, headers=headers, json=payload
    )
    _, data = helpers.err_check(
        response, (400, XboxLiveInvalidUserHash), (401, Unauthorized)
    )
    return data["access_token"]
