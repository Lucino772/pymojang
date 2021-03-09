import requests
import json
from urllib.parse import urljoin
from ..utils import TokenPair

class Yggdrasil:

    ROOT_URL = 'https://authserver.mojang.com'

    def __init__(self,session: requests.Session, token_pair: TokenPair):
        self._session = session
        self._token_pair = token_pair

        if self._token_pair.access_token is not None:
            self._session.headers.update({'Authorization': f'Bearer {self._token_pair.access_token}'})

    def authenticate(self, username: str, password: str):
        auth_url = urljoin(self.ROOT_URL, 'authenticate')
        payload = {
            'username': username,
            'password': password,
            'clientToken': self._token_pair.client_token
        }
        
        response = self._session.post(auth_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self._token_pair.update(access_token=data['accessToken'], client_token=data['clientToken'])
            self._session.headers.update({'Authorization': f'Bearer {self._token_pair.access_token}'})
        else:
            pass

    def refresh(self):
        refresh_url = urljoin(self.ROOT_URL, 'refresh')
        payload = {
            'accessToken': self._token_pair.access_token,
            'clientToken': self._token_pair.client_token
        }

        response = self._session.post(refresh_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self._token_pair.update(access_token=data['accessToken'], client_token=data['clientToken'])
            self._session.headers.update({'Authorization': f'Bearer {self._token_pair.access_token}'})
        else:
            pass

    def validate(self):
        validate_url = urljoin(self.ROOT_URL, 'validate')
        payload = {
            'accessToken': self._token_pair.access_token,
            'clientToken': self._token_pair.client_token
        }

        response = self._session.post(validate_url, json=payload)
        return response.status_code == 204

    def signout(self, username: str, password: str):
        signout_url = urljoin(self.ROOT_URL, 'signout')
        payload = {
            'username': username,
            'password': password
        }

        response = self._session.post(signout_url, json=payload)
        if response.status_code == 204:
            self._token_pair.update(access_token=None)
            self._session.headers.pop('Authorization')
            
            return True
        else:
            return False

    def invalidate(self):
        invalidate_url = urljoin(self.ROOT_URL, 'invalidate')
        payload = {
            'accessToken': self._token_pair.access_token,
            'clientToken': self._token_pair.client_token
        }

        response = self._session.post(invalidate_url, json=payload)
        if response.status_code == 204:
            self._token_pair.update(access_token=None)
            self._session.headers.pop('Authorization')
            
            return True
        else:
            return False
