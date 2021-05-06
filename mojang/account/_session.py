import datetime as dt
from dataclasses import dataclass, field

from . import session, user
from ._structures import UserProfile
from .auth import security, yggdrasil


def connect(username: str, password: str, client_token: str = None):
    auth = yggdrasil.authenticate(username, password, client_token)
    return UserSession(auth.access_token, auth.client_token)


@dataclass(init=False)
class UserSession(UserProfile):
    created_at: dt.datetime = field()
    name_change_allowed: bool = field()

    def __init__(self, access_token: str, client_token: str):
        self.__access_token = access_token
        self.__client_token = client_token

        self.refresh()

    def refresh(self):
        auth = yggdrasil.refresh(self.__access_token, self.__client_token)

        # Update tokens
        self.__access_token = auth.access_token
        self.__client_token = auth.client_token

        # Update info
        self.uuid = auth.uuid
        self.name = auth.name
        self.is_demo = auth.demo
        self.is_legacy = auth.legacy

        # Fetch other data
        self._fetch_data()

    def _fetch_data(self):
        # Load profile
        profile = user(self.uuid)
        self.names = profile.names
        self.skin = profile.skin
        self.cape = profile.cape
        del profile

        # Load name change
        name_change = session.get_user_name_change(self.__access_token)
        self.name_change_allowed = name_change.allowed
        self.created_at = name_change.created_at
    
    def close(self):
        yggdrasil.invalidate(self.__access_token, self.__client_token)
        self.__access_token = None
        self.__client_token = None

    @property
    def token_pair(self):
        return self.__access_token, self.__client_token

    # Security
    @property
    def secure(self):
        return security.check_ip(self.__access_token)

    @property
    def challenges(self):
        return security.get_challenges(self.__access_token)

    def verify(self, answers: list):
        return security.verify_ip(self.__access_token, answers)

    # Name
    def change_name(self, name: str):
        session.change_user_name(self.__access_token, name)
        self._fetch_data()

    # Skin
    def change_skin(self, path: str, variant='classic'):
        session.change_user_skin(self.__access_token, path, variant)
        self._fetch_data()

    def reset_skin(self):
        session.reset_user_skin(self.__access_token, self.uuid)
        self._fetch_data()
