"""
Mojang Yggdrasil authentication system api
"""

from ...error.exceptions import *
from ...utils import web
from ..urls import AUTHENTICATE, INVALIDATE, REFRESH, SIGNOUT, VALIDATE


def authenticate_user(username: str, password: str, client_token=None) -> dict:
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

def refresh_token(access_token: str, client_token: str):
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
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    web.request('post', VALIDATE, exceptions=(PayloadError, TokenError), json=payload)

def signout_user(username: str, password: str):
    payload = {
        'username': ctx.username,
        'password': ctx.password
    }

    web.request('post', SIGNOUT, exceptions=(PayloadError, CredentialsError), json=payload)

def invalidate_token(access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    web.request('post', INVALIDATE, exceptions=(PayloadError, TokenError), json=payload)
