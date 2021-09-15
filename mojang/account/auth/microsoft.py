import requests
from mojang.exceptions import *

from ..utils.auth import URLs

HEADERS_ACCEPT_JSON = {
    'content-type': 'application/json',
    'accept': 'application/json'
}


def authenticate_xbl(auth_token: str) -> tuple:
    """Authenticate with Xbox Live
    
    Args:
        auth_token (str): The access token received from the authentication with Microsoft
    
    Returns:
        A tuple containing the Xbox Live token and user hash

    Raises:
        XboxLiveAuthenticationError: If the auth token is invalid
    """

    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": "d={}".format(auth_token)
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }

    response = requests.post(URLs.microsoft_xbl_authenticate(), headers=HEADERS_ACCEPT_JSON, json=data)
    data = handle_response(response, XboxLiveAuthenticationError)
    return data['Token'], data['DisplayClaims']['xui'][0]['uhs']

def authenticate_xsts(xbl_token: str) -> tuple:
    """Retrieve the XSTS Token
    
    Args:
        xbl_token (str): The Xbox Live token
    
    Returns:
        A tuple containing the XSTS token and user hash

    Raises:
        XboxLiveAuthenticationError: If the xbl token is invalid
    """

    data = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xbl_token]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }

    response = requests.post(URLs.microsoft_xbl_authorize(), headers=HEADERS_ACCEPT_JSON, json=data)
    data = handle_response(response, XboxLiveAuthenticationError)
    return data['Token'], data['DisplayClaims']['xui'][0]['uhs']

def authenticate_minecraft(userhash: str, xsts_token: str):
    """Login to minecraft using Xbox Live
    Args:
        user_hash (str): The user hash from Xbox Live
        xbl_token (str): The XSTS Token from Xbox Live
    
    Returns:
        The minecraft access token

    Raises:
        XboxLiveInvalidUserHash: If the user hash is invalid
        Unauthorized: If the XSTS token is invalid
    """

    data = {"identityToken": f"XBL3.0 x={userhash};{xsts_token}"}

    response = requests.post(URLs.login_with_microsoft(), headers=HEADERS_ACCEPT_JSON, json=data)
    data = handle_response(response, XboxLiveInvalidUserHash, Unauthorized)
    return data['access_token']
