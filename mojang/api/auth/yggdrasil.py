import requests
from ..urls import AUTHENTICATE, REFRESH, VALIDATE, SIGNOUT, INVALIDATE
from ...error.handler import handle_response
from ...error.exceptions import *

def authenticate(session: requests.Session, username: str, password: str, client_token=None):
    payload = {
        'username': username,
        'password': password,
        'clientToken': client_token,
        'agent': {
            'name': 'Minecraft',
            'version': 1
        }
    }
    
    response = session.post(AUTHENTICATE, json=payload)
    data = handle_response(response, PayloadError, CredentialsError)
    session.headers.update({'Authorization': 'Bearer {}'.format(data['accessToken'])})

    # Parse response
    res = {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }
    return res

def refresh(session: requests.Session, access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session.post(REFRESH, json=payload)
    data = handle_response(response, PayloadError, TokenError)
    session.headers.update({'Authorization': 'Bearer {}'.format(data['accessToken'])})

    # Parse response
    res = {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }
    return res

def validate(session: requests.Session, access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session.post(VALIDATE, json=payload)
    handle_response(response, PayloadError, TokenError)
    return True

def signout(session: requests.Session, username: str, password: str):
    payload = {
        'username': username,
        'password': password
    }

    response = session.post(SIGNOUT, json=payload)
    data = handle_response(response, PayloadError, CredentialsError)
    session.headers.pop('Authorization')

def invalidate(session: requests.Session, access_token: str, client_token: str):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session.post(INVALIDATE, json=payload)
    handle_response(response, PayloadError, TokenError)
    session.headers.pop('Authorization')
