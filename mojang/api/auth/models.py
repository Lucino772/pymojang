import datetime
import enum
from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple, Union, overload

import msal

from mojang.exceptions import MicrosoftInvalidGrant, MicrosoftUserNotOwner

from .. import session
from ..auth import microsoft, security, yggdrasil
from ..models import Cape, Skin
from ..structures import ChallengeInfo

_DEFAULT_SCOPES = ["XboxLive.signin"]


# User
class AuthenticatedUser(metaclass=ABCMeta):
    """
    Base class for every authenticated user

    :param str access_token: The session token
    :param str refresh_token: The refresh token

    :var str name: The user name
    :var str uuid: The user uuid
    :var bool is_legacy: Wether the account has migrated
    :var bool is_demo: Wether the account is demo
    :var Skin skin: The active user skin
    :var List[Skin] skins: All the skins of the user
    :var Cape cape: The active user cape
    :var List[Cape] capes: All the capes of the user
    :var bool name_change_allowed:  Can the user change name
    :var datetime.datetime created_at: When was the user created
    """

    def __init__(self, access_token: str, refresh_token: str) -> None:
        self.__name = None
        self.__uuid = None
        self.__is_legacy = False
        self.__is_demo = False
        self.__skins = None
        self.__capes = None

        self.__name_change_allowed = False
        self.__created_at = None

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
    def name(self) -> Optional[str]:
        return self.__name

    @property
    def uuid(self) -> Optional[str]:
        return self.__uuid

    @property
    def is_legacy(self) -> bool:
        return self.__is_legacy

    @property
    def is_demo(self) -> bool:
        return self.__is_demo

    @property
    def skins(self) -> Optional[List[Skin]]:
        return self.__skins

    @property
    def skin(self) -> Optional[Skin]:
        if self.__skins is None:
            return None

        res = list(filter(lambda s: s.state == "ACTIVE", self.__skins))
        if len(res) > 0:
            return res[0]

        return None

    @property
    def capes(self) -> Optional[List[Cape]]:
        return self.__capes

    @property
    def cape(self) -> Optional[Cape]:
        if self.__capes is None:
            return None

        res = list(filter(lambda cape: cape.state == "ACTIVE", self.__capes))
        if len(res) > 0:
            return res[0]

        return None

    @property
    def name_change_allowed(self) -> bool:
        return self.__name_change_allowed

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        return self.__created_at

    def _fetch_profile(self):
        # Load profile
        profile = session.get_profile(self._access_token)
        self.__name = profile.name
        self.__uuid = profile.uuid
        self.__skins = profile.skins
        self.__capes = profile.capes
        self.__is_legacy = profile.is_legacy
        self.__is_demo = profile.is_demo
        del profile

        # Load name change
        name_change = session.get_user_name_change(self._access_token)
        self.__name_change_allowed = name_change.allowed
        self.__created_at = name_change.created_at

    def change_name(self, name: str):
        """Change user name. For more details checkout :py:meth:`~mojang.account.session.change_user_name`

        :param str name: The new name
        """
        session.change_user_name(self._access_token, name)
        self._fetch_profile()

    def change_skin(self, path: str, variant: Optional[str] = "classic"):
        """Change user skin. For more details checkout :py:meth:`~mojang.account.session.change_user_skin`

        :param str path: The path to the skin, either local or remote
        :param str variant: The variant of skin (default to 'classic')
        """
        session.change_user_skin(self._access_token, path, variant)
        self._fetch_profile()

    def reset_skin(self):
        """Reset user skin. For more details checkout :py:meth:`~mojang.account.session.reset_user_skin`"""
        session.reset_user_skin(self._access_token)
        self._fetch_profile()

    def show_cape(self, cape_index: int = 0):
        """Show user cape. For more details checkout :py:meth:`~mojang.account.session.show_user_cape`

        :param int cape: The index of the cape
        """
        if not isinstance(self.capes, list):
            return

        if len(self.capes) == 0:
            return

        cape = self.capes[cape_index]
        if isinstance(cape.id, str):
            session.show_user_cape(self._access_token, cape.id)

    def hide_cape(self):
        """Hide user cape. For more details checkout :py:meth:`~mojang.account.session.hide_user_cape`"""
        session.hide_user_cape(self._access_token)


class MojangAuthenticatedUser(AuthenticatedUser):
    """Class for user with a Mojang account"""

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
    def secure(self) -> bool:
        """Check wether user IP is secured. For more details checkout :py:meth:`~mojang.account.auth.security.check_ip`"""
        return security.check_ip(self._access_token)

    @property
    def challenges(self) -> List[ChallengeInfo]:
        """Returns the list of challenges to verify user IP. For more details checkout :py:meth:`~mojang.account.auth.security.get_challenges`"""
        return security.get_challenges(self._access_token)

    def verify(self, answers: list) -> bool:
        """Verify user IP. For more details checkout :py:meth:`~mojang.account.auth.security.verify_ip`"""
        return security.verify_ip(self._access_token, answers)


class MicrosoftAuthenticatedUser(AuthenticatedUser):
    """Class for user with a Microsoft account"""

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


# Authentication
class MojangAuthenticationApp:
    def __init__(
        self, client: msal.ClientApplication, redirect_uri: str
    ) -> None:
        self.__client = client
        self.__redirect_uri = redirect_uri

    @property
    def authorization_url(self) -> str:
        """Returns the authorization url for Microsoft OAuth"""
        return self.__client.get_authorization_request_url(
            scopes=_DEFAULT_SCOPES,
            redirect_uri=(self.__redirect_uri),
        )

    def _acquire_microsoft_token(self, code: str) -> Tuple[str, str]:
        response = self.__client.acquire_token_by_authorization_code(
            code,
            scopes=_DEFAULT_SCOPES,
            redirect_uri=(self.__redirect_uri),
        )
        if response.get("error", False):
            raise MicrosoftInvalidGrant(*response.values())

        xbl_token, userhash = microsoft.authenticate_xbl(
            response["access_token"]
        )
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        access_token = microsoft.authenticate_minecraft(userhash, xsts_token)

        if not session.owns_minecraft(access_token):
            raise MicrosoftUserNotOwner()

        return access_token, str(response["refresh_token"])

    @overload
    def get_session(
        self, username: str, password: str, client_token: str = None
    ) -> MojangAuthenticatedUser:
        """Authenticate with a Mojang Account

        :param str username: The username of email if account is not legacy
        :param str password: The user password
        :param client_token: The client token to use
        :type client_token: str or None

        :Examples:

        .. code-block:: python

            import mojang

            CLIENT_ID = ... # Your Azure App client id
            CLIENT_SECRET = ... # Your Azure App client secret

            app = mojang.app(CLIENT_ID, CLIENT_SECRET)
            user = app.get_session("USERNAME", "PASSWORD")
        """
        ...

    @overload
    def get_session(self, code: str) -> MicrosoftAuthenticatedUser:
        """Authenticate with a Microsoft Account

        :param str auth_code: The auth code from the redirect

        :raises MicrosoftInvalidGrant: if auth code is invalid

        :Examples:

        .. code-block:: python

            import mojang

            CLIENT_ID = ... # Your Azure App client id
            CLIENT_SECRET = ... # Your Azure App client secret

            app = mojang.app(CLIENT_ID, CLIENT_SECRET)

            # To authenticate users, you first need them to visit the url
            # returned by the function `app.authorization_url`
            print(app.authorization_url)

            # Once they will have granted access to their account to your app,
            # they will be redirect to the uri you choose with a `code` parameter
            # http://example.com?code=...
            # You can use this code to authenticate the user
            code = ...
            user = app.get_session(code)
        """
        ...

    def get_session(
        self, *args, **kwargs
    ) -> Union[MojangAuthenticatedUser, MicrosoftAuthenticatedUser, None]:
        if len(args) == 2:
            access_token, refresh_token = yggdrasil.authenticate(
                args[0], args[1], kwargs.get("client_token", None)
            )
            return MojangAuthenticatedUser(access_token, refresh_token)
        elif len(args) == 1:
            access_token, refresh_token = self._acquire_microsoft_token(
                args[0]
            )
            return MicrosoftAuthenticatedUser(
                access_token, refresh_token, self.__client
            )

        return None
