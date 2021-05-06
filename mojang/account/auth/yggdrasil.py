import requests

from ...exceptions import *
from .._structures import AuthenticationInfo
from ._urls import URLs


def authenticate(username: str, password: str, client_token: str = None):
    payload = {
        'username': username,
        'password': password,
        'clientToken': client_token,
        'agent': {
            'name': 'Minecraft',
            'version': 1
        }
    }
    response = requests.post(URLs.authenticate(), json=payload)
    data = handle_response(response, PayloadError, CredentialsError)

    _dict = {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }
    return AuthenticationInfo(**_dict)

def refresh(access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post(URLs.refresh(), json=payload)
    data = handle_response(response, PayloadError, TokenError)

    _dict = {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }
    return AuthenticationInfo(**_dict)

def validate(access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post(URLs.validate(), json=payload)
    handle_response(response, PayloadError, TokenError)

def signout(username: str, password: str):
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(URLs.signout(), json=payload)
    handle_response(response, PayloadError, CredentialsError)

def invalidate(access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post(URLs.invalidate(), json=payload)
    data = handle_response(response, PayloadError, TokenError)
