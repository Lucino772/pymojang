import datetime as dt
from typing import Callable, Optional, Tuple

from .. import session
from ..auth import security, yggdrasil
from ..structures.base import NameInfoList
from ..structures.session import Cape, Skin


def _refresh_method(access_token: str, client_token: str):
    auth = yggdrasil.refresh(access_token, client_token)
    return auth.access_token, auth.client_token


def connect(username: str, password: str, client_token: Optional[str] = None) -> 'UserSession':
    """Connect a user with name and password
    
    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password
        client_token (str, optional): The client token to use in the authentication (default to None)
    
    Returns:
        UserSession

    Example:

        ```python
        import mojang

        session = mojang.connect('USERNAME_OR_EMAIL', 'PASSWORD')
        print(session)
        ```
        ```bash
        UserSession(
            name='PLAYER_NAME', 
            uuid='PLAYER_UUID', 
            is_legacy=False, 
            is_demo=False, 
            names=(NameInfo(name='PLAYER_NAME', changed_to_at=None),), 
            skin=Skin(source='http://...', variant='classic'), 
            cape=None, 
            created_at=datetime.datetime(2006, 4, 29, 10, 10, 10), 
            name_change_allowed=True
        )
        ```
    """
    auth = yggdrasil.authenticate(username, password, client_token)
    return UserSession(auth.access_token, auth.client_token, False, _refresh_method, yggdrasil.invalidate)


class UserSession:
    """
    Attributes:
        name (str): The user name
        uuid (str): The user uuid
        is_legacy (bool): Wether the account has migrated
        is_demo (bool): Wether the account is demo
        names (NameInfoList): The user name history
        skin (Skin): The user skin
        cape (Cape): The user cape
        name_change_allowed (bool): Wether the user can change name
        created_at (dt.datetime): When was the user created
    """
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    names: NameInfoList
    skin: Skin
    cape: Cape
    created_at: dt.datetime
    name_change_allowed: bool

    def __init__(self, access_token: str, client_token: str, has_migrated: bool, refresh_method: Callable[[str, str], Tuple], close_method: Callable[[str, str], Tuple]):
        self.__access_token = access_token
        self.__client_token = client_token
        self.__refresh_method = refresh_method
        self.__close_method = close_method

        self.__has_migrated = has_migrated
        self._fetch_profile()

    def refresh(self):
        """Refresh the session's token"""
        if callable(self.__refresh_method):
            self.__access_token, self.__client_token = self.__refresh_method(self.__access_token, self.__client_token)
        
        self._fetch_profile()

    def _fetch_profile(self):
        # Load profile
        profile = session.get_profile(self.__access_token)
        self.name = profile.name
        self.uuid = profile.uuid
        self.names = profile.names
        self.skin = profile.skin
        self.cape = profile.cape
        self.is_demo = profile.is_demo
        self.is_legacy = profile.is_legacy
        del profile

        # Load name change
        name_change = session.get_user_name_change(self.__access_token)
        self.name_change_allowed = name_change.allowed
        self.created_at = name_change.created_at

    def close(self):
        """Close the session and invalidates the access token"""
        if callable(self.__close_method):
            self.__close_method(self.__access_token, self.__client_token)
        
        self.__access_token = None
        self.__client_token = None

    @property
    def token_pair(self) -> Tuple[str, str]:
        """Returns the access token and the client token"""
        return self.__access_token, self.__client_token

    # Security
    @property
    def secure(self):
        """Check wether user IP is secured. For more details checkout [`check_ip`][mojang.account.auth.security.check_ip]"""
        if not self.__has_migrated:
            return security.check_ip(self.__access_token)

        return True

    @property
    def challenges(self):
        """Returns the list of challenges to verify user IP. For more details checkout [`get_challenges`][mojang.account.auth.security.get_challenges]"""
        if not self.__has_migrated:
            return security.get_challenges(self.__access_token)

        return []

    def verify(self, answers: list):
        """Verify user IP. For more details checkout [`verify_ip`][mojang.account.auth.security.verify_ip]"""
        if not self.__has_migrated:
            return security.verify_ip(self.__access_token, answers)

    # Name
    def change_name(self, name: str):
        """Change user name. For more details checkout [`change_user_name`][mojang.account.session.change_user_name]
        
        Args:
            name (str): The new name
        """
        session.change_user_name(self.__access_token, name)
        self._fetch_profile()

    # Skin
    def change_skin(self, path: str, variant: Optional[str] = 'classic'):
        """Change user skin. For more details checkout [`change_user_skin`][mojang.account.session.change_user_skin]

        Args:
            path (str): The path to the skin, either local or remote
            variant (str, optional): The variant of skin (default to 'classic')
        """
        session.change_user_skin(self.__access_token, path, variant)
        self._fetch_profile()

    def reset_skin(self):
        """Reset user skin. For more details checkout [`reset_user_skin`][mojang.account.session.reset_user_skin]"""
        session.reset_user_skin(self.__access_token, self.uuid)
        self._fetch_profile()
