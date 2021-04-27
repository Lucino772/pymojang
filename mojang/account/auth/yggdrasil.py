import requests

from ._urls import URLs
from .._structures import AuthenticationInfo

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

    data = response.json()
    _dict = {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }
    return AuthenticationInfo(**_dict)

def refresh(access_token: str, client_token: str) -> dict:
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post(URLs.refresh(), json=payload)

    data = response.json()
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

def signout(username: str, password: str):
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(URLs.signout(), json=payload)

def invalidate(access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post(URLs.invalidate(), json=payload)
