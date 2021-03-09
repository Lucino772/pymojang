import requests
import os
import datetime as dt
from urllib.parse import urljoin
from . import api
from .profile import UserProfile
from ..auth import Yggdrasil, SecurityCheck
from ..utils import TokenPair

class UserSession:

    MINECRAFT_SERVICE_URL = 'https://api.minecraftservices.com'

    def __init__(self, username: str, password: str, token_file=None):
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})

        self._username = username
        self._password = password

        self.token_pair = TokenPair(None, None)
        if isinstance(token_file, str) and os.path.exists(token_file):
            self.token_pair = TokenPair.from_pickle(token_file)

        self._auth = Yggdrasil(self._session, self.token_pair)
        self._security = SecurityCheck(self._session)
        self._profile = UserProfile()

        self._security_challenges = self._security.challenges

    def connect(self):
        if self.token_pair.access_token is not None:
            if not self._auth.validate():
                self._auth.refresh()
        else:
            self._auth.authenticate(self._username, self._password)
        
        self._load_user_data()

    def disconnect(self):
        return self._auth.invalidate()

    def save(self, filename: str):
        self.token_pair.to_pickle(filename)

    @property
    def profile(self):
        return self._profile

    # Security questions/answers
    @property
    def must_check_security(self):
        return not self._security.ok

    @property
    def security_challenges(self):
        return self._security_challenges

    def send_security_answers(self, answers: list):
        return self._security.send_answers(answers)

    # User data
    def _load_user_data(self):
        self._get_name_change()
        self._get_profile()
        
        self._profile.names = api.get_name_history(self._profile.id)

    def _get_name_change(self):
        name_change_url = urljoin(self.MINECRAFT_SERVICE_URL, 'minecraft/profile/namechange')
        response = self._session.get(name_change_url)

        if response.status_code == 200:
            data = response.json()
            self._profile.created_at = dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
            self._profile.name_change_allowed = data['nameChangeAllowed']
        else:
            pass
    
    def _get_profile(self):
        profile_url = urljoin(self.MINECRAFT_SERVICE_URL, 'minecraft/profile')
        response = self._session.get(profile_url)

        if response.status_code == 200:
            data = response.json()
            self._profile.id = data['id']
            self._profile.name = data['name']

            for skin in data['skins']:
                self._profile.skins.append({
                    'url': skin['url'],
                    'variant': skin['variant'].lower()
                })
            
            for cape in data['capes']:
                self._profile.capes.append({
                    'url': cape['url']
                })
        else:
            pass
