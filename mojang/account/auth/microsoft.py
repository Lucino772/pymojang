from typing import Tuple

import requests
from mojang.exceptions import (
    Unauthorized,
    XboxLiveAuthenticationError,
    XboxLiveInvalidUserHash,
    handle_response,
)

from ..utils import helpers, urls


def authenticate_xbl(auth_token: str) -> Tuple[str, str]:
    """Authenticate with Xbox Live using the Microsoft access token
    received after the OAuth authentication

    Args:
        auth_token (str): The access token

    Returns:
        A tuple containing the Xbox Live token and user hash

    Raises:
        XboxLiveAuthenticationError: If the auth token is invalid
    """
    headers = helpers.get_headers(json_content=True)
    data = {
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
        json=data,
    )
    data = handle_response(response, XboxLiveAuthenticationError)
    return data["Token"], data["DisplayClaims"]["xui"][0]["uhs"]


def authenticate_xsts(xbl_token: str) -> Tuple[str, str]:
    """Retrieve the XSTS Token using the Xbox Live token

    Args:
        xbl_token (str): The Xbox Live token

    Returns:
        A tuple containing the XSTS token and user hash

    Raises:
        XboxLiveAuthenticationError: If the xbl token is invalid
    """
    headers = helpers.get_headers(json_content=True)
    data = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    }

    response = requests.post(
        urls.api_ms_xbl_authorize, headers=headers, json=data
    )
    data = handle_response(response, XboxLiveAuthenticationError)
    return data["Token"], data["DisplayClaims"]["xui"][0]["uhs"]


def authenticate_minecraft(userhash: str, xsts_token: str) -> str:
    """Retrieve the Minecraft access token loging in using Xbox Live

    Args:
        userhash (str): The user hash from Xbox Live
        xsts_token (str): The XSTS Token from Xbox Live

    Returns:
        The minecraft access token

    Raises:
        XboxLiveInvalidUserHash: If the user hash is invalid
        Unauthorized: If the XSTS token is invalid

    Example:

        ```python
        from mojang.account.auth import microsoft

        ACCESS_TOKEN = '....' # Access token from Microsoft

        xbl_token, _ = microsoft.authenticate_xbl(ACCESS_TOKEN)
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        mc_access_token = microsoft.authenticate_minecraft(userhash, xsts_token)
        ```
    """
    headers = helpers.get_headers(json_content=True)
    data = {"identityToken": f"XBL3.0 x={userhash};{xsts_token}"}

    response = requests.post(urls.api_ms_xbl_login, headers=headers, json=data)
    data = handle_response(response, XboxLiveInvalidUserHash, Unauthorized)
    return data["access_token"]
