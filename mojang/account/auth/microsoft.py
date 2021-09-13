import requests
from mojang.exceptions import *

from ..utils.auth import URLs


HEADERS_ACCEPT_URL_ENCODED = {
    'content-type': 'application/x-www-form-urlencoded'
}

HEADERS_ACCEPT_JSON = {
    'content-type': 'application/json',
    'accept': 'application/json'
}


def get_login_url(client_id: str, redirect_uri: str = 'http://example.com') -> str:
    """Returns the login url for the browser
    
    Args:
        client_id (str): Azure Active Directory App's client id
        redirect_uri (str, optional): The redirect uri of your application
    """
    return URLs.microsoft_authorize(client_id, redirect_uri)


def authorize(client_id: str, client_secret: str, auth_code: str, redirect_uri: str = 'http://example.com') -> tuple:
    """Retrieve the access token and refresh token from the given auth code
    
    Args:
        client_id (str): Azure Active Directory App's client id
        client_secret (str): Azure Active Directory App's client secret
        auth_code (str): The auth code received from the login url
        redirect_uri (str, optional): The redirect uri of your application
    
    Returns:
        A tuple containing the access token and refresh token

    Raises:
        MicrosoftInvalidGrant: If the auth code is invalid
    """

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    response = requests.post(URLs.microsoft_token(), headers=HEADERS_ACCEPT_URL_ENCODED, data=data)
    data = handle_response(response, MicrosoftInvalidGrant)
    
    return data['access_token'], data['refresh_token']

def refresh(client_id: str, client_secret: str, refresh_token: str, redirect_uri: str = 'http://example.com') -> tuple:
    """Refresh an access token
    
    Args:
        client_id (str): Azure Active Directory App's client id
        client_secret (str): Azure Active Directory App's client secret
        refresh_token (str): The refresh token
        redirect_uri (str, optional): The redirect uri of your application
    
    Returns:
        A tuple containing the access token and refresh token

    Raises:
        MicrosoftInvalidGrant: If the auth code is invalid
    """

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'redirect_uri': redirect_uri
    }

    response = requests.post(URLs.microsoft_token(), headers=HEADERS_ACCEPT_URL_ENCODED, data=data)
    data = handle_response(response, MicrosoftInvalidGrant)
    
    return data['access_token'], data['refresh_token']


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
