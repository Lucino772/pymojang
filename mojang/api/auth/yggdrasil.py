"""
Mojang Yggdrasil authentication system api
"""

from ...error.exceptions import *
from ...utils import web
from ..urls import AUTHENTICATE, INVALIDATE, REFRESH, SIGNOUT, VALIDATE


def authenticate_user(username: str, password: str, client_token: str = None) -> dict:
    """Authenticate user with name and password

    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password
        client_token (str, optional): The client token to use in the authentication (default to None)

    Returns:
        A dict with thet following keys : `access_token`, `client_token`, `uuid`, `name`, 
        `legacy` and `demo` 

    Raises:
        CredentialsError: If username and password are invalid
        PayloadError: If credentials are not formated correctly
    """
    payload = {
        'username': username,
        'password': password,
        'clientToken': client_token,
        'agent': {
            'name': 'Minecraft',
            'version': 1
        }
    }

    data = web.request('post', AUTHENTICATE, exceptions=(PayloadError, CredentialsError), json=payload)

    return {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }

def refresh_token(access_token: str, client_token: str) -> dict:
    """Refresh an invalid access token

    Args:
        access_token (str): The access token to refresh
        client_token (str): The client token used to generate the access token

    Returns:
        A dict with the following keys: `access_token`, `client_token`, `uuid`, `name`,
        `legacy` and `demo` 

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly
    """
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    data = web.request('post', REFRESH, exceptions=(PayloadError, TokenError), json=payload)

    return {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }

def validate_token(access_token: str, client_token: str):
    """Validate an access token

    Args:
        access_token (str): The access token to validate
        client_token (str): The client token used to generate the access token

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly
    """
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    web.request('post', VALIDATE, exceptions=(PayloadError, TokenError), json=payload)

def signout_user(username: str, password: str):
    """Signout user with name and password

    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password

    Raises:
        CredentialsError: If username and password are invalid
        PayloadError: If credentials are not formated correctly
    """
    payload = {
        'username': ctx.username,
        'password': ctx.password
    }

    web.request('post', SIGNOUT, exceptions=(PayloadError, CredentialsError), json=payload)

def invalidate_token(access_token: str, client_token: str):
    """Invalidate an access token

    Args:
        access_token (str): The access token to invalidate
        client_token (str): The client token used to generate the access token

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly
    """
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    web.request('post', INVALIDATE, exceptions=(PayloadError, TokenError), json=payload)
