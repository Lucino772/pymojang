import datetime as dt
from typing import Optional, Tuple

from ..structures.session import Cape, Skin

from .. import session, user
from ..auth import security, yggdrasil
from ..structures.base import NameInfoList


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
    return UserSession(auth.access_token, auth.client_token)



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

    def __init__(self, access_token: str, client_token: str):
        """Create a user session with access token and client token.
        The access token will be refreshed once the class is initiated

        Args:
            access_token (str): The session's access token
            client_token (str): The session's client token
        """
        self.__access_token = access_token
        self.__client_token = client_token

        self.refresh()

    def refresh(self):
        """Refresh the full user session, including the data"""
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
        """Close the session and invalidates the access token"""
        yggdrasil.invalidate(self.__access_token, self.__client_token)
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
        return security.check_ip(self.__access_token)

    @property
    def challenges(self):
        """Returns the list of challenges to verify user IP. For more details checkout [`get_challenges`][mojang.account.auth.security.get_challenges]"""
        return security.get_challenges(self.__access_token)

    def verify(self, answers: list):
        """Verify user IP. For more details checkout [`verify_ip`][mojang.account.auth.security.verify_ip]"""
        return security.verify_ip(self.__access_token, answers)

    # Name
    def change_name(self, name: str):
        """Change user name. For more details checkout [`change_user_name`][mojang.account.session.change_user_name]
        
        Args:
            name (str): The new name
        """
        session.change_user_name(self.__access_token, name)
        self._fetch_data()

    # Skin
    def change_skin(self, path: str, variant: Optional[str] = 'classic'):
        """Change user skin. For more details checkout [`change_user_skin`][mojang.account.session.change_user_skin]

        Args:
            path (str): The path to the skin, either local or remote
            variant (str, optional): The variant of skin (default to 'classic')
        """
        session.change_user_skin(self.__access_token, path, variant)
        self._fetch_data()

    def reset_skin(self):
        """Reset user skin. For more details checkout [`reset_user_skin`][mojang.account.session.reset_user_skin]"""
        session.reset_user_skin(self.__access_token, self.uuid)
        self._fetch_data()
