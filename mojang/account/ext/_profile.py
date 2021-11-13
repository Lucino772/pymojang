from abc import ABCMeta, abstractmethod
from typing import Optional

import msal

from .. import session
from ..auth import microsoft, security, yggdrasil


class AuthenticatedUser(metaclass=ABCMeta):
    def __init__(self, access_token: str, refresh_token: str) -> None:
        self.__name = None
        self.__uuid = None
        self.__is_legacy = False
        self.__is_demo = False
        self.__names = None
        self.__skin = None
        self.__cape = None

        self.__name_change_allowed = False
        self.__created_at = False

        self._access_token = access_token
        self._refresh_token = refresh_token

        self._fetch_profile()

    @abstractmethod
    def refresh(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.__name

    @property
    def uuid(self):
        return self.__uuid

    @property
    def is_legacy(self):
        return self.__is_legacy

    @property
    def is_demo(self):
        return self.__is_demo

    @property
    def names(self):
        return self.__names

    @property
    def skin(self):
        return self.__skin

    @property
    def cape(self):
        return self.__cape

    @property
    def name_change_allowed(self):
        return self.__name_change_allowed

    @property
    def created_at(self):
        return self.__created_at

    def _fetch_profile(self):
        # Load profile
        profile = session.get_profile(self._access_token)
        self.__name = profile.name
        self.__uuid = profile.uuid
        self.__names = profile.names
        self.__skin = profile.skin
        self.__cape = profile.cape
        self.__is_legacy = profile.is_legacy
        self.__is_demo = profile.is_demo
        del profile

        # Load name change
        name_change = session.get_user_name_change(self._access_token)
        self.__name_change_allowed = name_change.allowed
        self.__created_at = name_change.created_at

    def change_name(self, name: str):
        """Change user name. For more details checkout [`change_user_name`][mojang.account.session.change_user_name]

        Args:
            name (str): The new name
        """
        session.change_user_name(self._access_token, name)
        self._fetch_profile()

    def change_skin(self, path: str, variant: Optional[str] = "classic"):
        """Change user skin. For more details checkout [`change_user_skin`][mojang.account.session.change_user_skin]

        Args:
            path (str): The path to the skin, either local or remote
            variant (str, optional): The variant of skin (default to 'classic')
        """
        session.change_user_skin(self._access_token, path, variant)
        self._fetch_profile()

    def reset_skin(self):
        """Reset user skin. For more details checkout [`reset_user_skin`][mojang.account.session.reset_user_skin]"""
        session.reset_user_skin(self._access_token, self.uuid)
        self._fetch_profile()


class MojangAuthenticatedUser(AuthenticatedUser):
    """
    Attributes:
        name (str): The user name
        uuid (str): The user uuid
        is_legacy (bool): Wether the account has migrated
        is_demo (bool): Wether the account is demo
        names (NameInfoList): The user name history
        skin (Skin): The user skin
        cape (Cape): The user cape
        name_change_allowed (bool): Can the user change name
        created_at (dt.datetime): When was the user created
    """

    def refresh(self):
        """Refresh current session"""
        self._access_token, self._refresh_token = yggdrasil.refresh(
            self._access_token, self._refresh_token
        )

    def close(self):
        """Close current session"""
        yggdrasil.invalidate(self._access_token, self._refresh_token)
        self._access_token, self._refresh_token = None

    @property
    def secure(self):
        """Check wether user IP is secured. For more details checkout [`check_ip`][mojang.account.auth.security.check_ip]"""
        return security.check_ip(self._access_token)

    @property
    def challenges(self):
        """Returns the list of challenges to verify user IP. For more details checkout [`get_challenges`][mojang.account.auth.security.get_challenges]"""
        return security.get_challenges(self._access_token)

    def verify(self, answers: list):
        """Verify user IP. For more details checkout [`verify_ip`][mojang.account.auth.security.verify_ip]"""
        return security.verify_ip(self._access_token, answers)


class MicrosoftAuthenticatedUser(AuthenticatedUser):
    """
    Attributes:
        name (str): The user name
        uuid (str): The user uuid
        is_legacy (bool): Wether the account has migrated
        is_demo (bool): Wether the account is demo
        names (NameInfoList): The user name history
        skin (Skin): The user skin
        cape (Cape): The user cape
        name_change_allowed (bool): Can the user change name
        created_at (dt.datetime): When was the user created
    """

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        oauth_client: msal.ClientApplication,
    ) -> None:
        super().__init__(access_token, refresh_token)
        self.__oauth_client = oauth_client

    def refresh(self):
        """Refresh current session"""
        response = self.__oauth_client.acquire_token_by_refresh_token(
            self._refresh_token, ["XboxLive.signin"]
        )
        xbl_token, userhash = microsoft.authenticate_xbl(
            response["access_token"]
        )
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        mc_token = microsoft.authenticate_minecraft(userhash, xsts_token)

        self._access_token, self._refresh_token = (
            mc_token,
            response["refresh_token"],
        )

    def close(self):
        """Close current session"""
        self._access_token, self._refresh_token = None, None
