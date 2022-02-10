import msal

from mojang.exceptions import MicrosoftInvalidGrant, MicrosoftUserNotOwner

from .. import session
from ..auth import microsoft
from ._profile import MicrosoftAuthenticatedUser

_DEFAULT_SCOPES = ["XboxLive.signin"]


def microsoft_app(
    client_id: str,
    client_secret: str,
    redirect_uri: str = "http://example.com",
) -> "MicrosoftApp":
    """It create an instance of :py:class:`~mojang.account.ext.microsoft.MicrosoftApp` with the client id and client secret.
    This app can then be used to get a :py:class:`mojang.account.ext._profile.MicrosoftAuthenticatedUser`.

    :param str client_id: Azure App client id
    :param str client_secret: Azure App client secret
    :param str redirect_uri: The default redirect uri for your app

    :Examples:

    .. code-block:: python

        import mojang

        CLIENT_ID = ... # Your Azure App client id
        CLIENT_SECRET = ... # Your Azure App client secret

        app = mojang.microsoft_app(CLIENT_ID, CLIENT_SECRET)

        # To authenticate users, you first need them to visit the url
        # returned by the function `app.authorization_url`
        url = app.authorization_url()

        # Once they will have granted access to their account to your app,
        # they will be redirect to the uri you choose with a `code` parameter
        # http://example.com?code=...
        # You can use this code to authenticate the user
        code = ...
        user = app.authenticate(code)
    """
    client = msal.ClientApplication(
        client_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/consumers",
    )
    return MicrosoftApp(client, redirect_uri)


class MicrosoftApp:
    """This class allows you to authenticate Microsoft users to Minecraft

    :param msal.ClientApplication client: The msal client
    :param str redirect_uri: The default redirect uri for your app
    """

    def __init__(self, client: msal.ClientApplication, redirect_uri: str):
        self.__client = client
        self.__redirect_uri = redirect_uri

    def authorization_url(self, redirect_uri: str = None) -> str:
        """Returns the authorization url for Microsoft OAuth"""
        return self.__client.get_authorization_request_url(
            scopes=_DEFAULT_SCOPES,
            redirect_uri=(redirect_uri or self.__redirect_uri),
        )

    def authenticate(
        self, auth_code: str, redirect_uri: str = None
    ) -> "MicrosoftAuthenticatedUser":
        """Authenticate a user with the auth code

        :param str auth_code: The auth code from the redirect
        :param str redirect_uri: If set overwrite your app's redirect uri

        :raises MicrosoftInvalidGrant: if auth code is invalid
        """
        response = self.__client.acquire_token_by_authorization_code(
            auth_code,
            scopes=_DEFAULT_SCOPES,
            redirect_uri=(redirect_uri or self.__redirect_uri),
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

        return MicrosoftAuthenticatedUser(
            access_token, response["refresh_token"], self.__client
        )
