import requests
from . import yggdrasil
from . import security
from ..user.profile import UserProfile
from ..urls import MINECRAFT_SERVICES, MOJANG_API
from ..user.skin import Skin


class UserSession:

    def __init__(self, username: str, password: str):
        self.__session = requests.Session()
        self.__session.headers.update({'Content-Type': 'application/json'})

        self.__access_token = None
        self.__client_token = None

        self.__username = username
        self.__password = password

        self.__profile = None

    def _request(self, method: str, url: str, **kwargs):
        _fct = getattr(self.__session, method)
        return _fct(url, **kwargs)

    def _update_token(self, **kwargs):
        self.__access_token = kwargs.get('access_token', self.__access_token)
        self.__client_token = kwargs.get('client_token', self.__client_token)
        if self.__access_token is None:
            self.__session.headers.pop('Authorization')
        else:
            self.__session.headers.update({'Authorization': f'Bearer {self.__access_token}'})
    
    # Connection / Disconnection
    def connect(self):
        if self.__password is not None:
            yggdrasil.authenticate(self, self.__username, self.__password)
            if self.secure:
                self.__profile = UserProfile(self.__session, authenticated=self.secure, load=True)

    def close(self):
        yggdrasil.invalidate(self, self.__access_token, self.__client_token)

    def close_all(self):
        yggdrasil.signout(self, self.__username, self.__password)

    # Security
    @property
    def secure(self):
        return security.is_secure(self)
    
    @property
    def challenges(self):
        return security.get_challenges(self)

    def verify(self, answers: list):
        return security.verify_ip(self, answers)

    # Other
    @property
    def profile(self):
        return self.__profile

    # Name
    def change_name(self, name: str):
        url = MINECRAFT_SERVICES.join('minecraft/profile/name/{}'.format(name))
        response = self.__session.put(url)

        if response.status_code == 204:
            self.__profile = UserProfile(self.__session, authenticated=self.secure, load=True)

    # Skin
    def upload_skin(self, path: str, variant='classic'):
        url = MINECRAFT_SERVICES.join('minecraft/profile/skins')
        skin = Skin(path, variant=variant)
        skin_data = skin.data
        
        files = [
            ('variant', variant),
            ('file', (f'image.{skin.extension[1:]}', skin_data, f'image/{skin.extension[1:]}'))
        ]
        response = self.__session.post(url, files=files, headers={'Content-Type': None})
        self.__profile = UserProfile(self.__session, authenticated=self.secure, load=True)
        return response.status_code == 200

    def reset_skin(self):
        url = MOJANG_API.join('user/profile/{}/skin'.format(self.profile.uuid))
        response = self.__session.delete(url)
        self.__profile = UserProfile(self.__session, authenticated=self.secure, load=True)
        return response.status_code == 204


def user(username: str, password: str):
    return UserSession(username, password)
