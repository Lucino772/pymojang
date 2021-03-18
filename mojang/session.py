import requests
from .api.auth import yggdrasil
from .api import security
from .api import user
from .api import base

from .profile import UserProfile

class UserSession:

    def __init__(self, session: requests.Session):
        self.__session = session
        self.__access_token = None
        self.__client_token = None
        self.__profile = None

    def connect(self, username: str, password: str):
        auth_data = yggdrasil.authenticate(self.__session, username, password)
        self.__access_token = auth_data.pop('access_token')
        self.__client_token = auth_data.pop('client_token')

        names = base.names(auth_data['uuid'])
        name_change_data = user.check_name_change(self.__session)
        profile_data = user.get_profile(self.__session)

        data = {'names': names, **auth_data, **name_change_data, ** profile_data}
        self.__profile = UserProfile(**data)

    def close(self):
        return yggdrasil.invalidate(self.__session, self.__access_token, self.__client_token)

    @property
    def profile(self):
        return self.__profile

    # Security
    @property
    def secure(self):
        return security.is_secure(self.__session)

    @property
    def challenges(self):
        return security.get_challenges(self.__session)

    def verify(self, answers: list):
        return security.verify_ip(self.__session, answers)
    
    # Name
    def change_name(self, name: str):
        user.change_name(self.__session, name)
        names = base.names(self.__profile.uuid)
        name_change_data = user.check_name_change(self.__session)
        self.__profile.update(name=name, names=names, **name_change_data)

    # Skin
    def change_skin(self, path: str, variant='classic'):
        user.upload_skin(self.__session, path, variant)
        profile_data = user.get_profile(self.__session)
        self.__profile.update(**profile_data)

    def reset_skin(self):
        user.reset_skin(self.__session)
        profile_data = user.get_profile(self.__session)
        self.__profile.update(**profile_data)