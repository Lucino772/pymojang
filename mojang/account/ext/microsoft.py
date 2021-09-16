from mojang.exceptions import MicrosoftInvalidGrant, MicrosoftUserNotOwner
import msal
from ..auth import microsoft
from .session import UserSession
from .. import session


_DEFAULT_SCOPES = ['XboxLive.signin']

def microsoft_app(client_id: str, client_secret: str, redirect_uri: str = 'http://example.com') -> 'MicrosoftApp':
    """It create an instance of [`MicrosoftApp`][mojang.account.ext.microsoft.MicrosoftApp] with the client id and client secret.
    This app can then be used to get a [`UserSession`][mojang.account.ext.session.UserSession] like 
    [`connect`][mojang.account.ext.session.connect] for Microsoft users.

    Args:
        client_id (str): Your Azure App client id
        client_secret (str): Your Azure App client secret
        redirect_uri (str, optional): The default redirect uri for your app

    Returns:
        An instance of the MicrosoftApp

    Examples:

        ```python
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
        ```
    """
    client = msal.ClientApplication(client_id, client_credential=client_secret, authority='https://login.microsoftonline.com/consumers')
    return MicrosoftApp(client, redirect_uri)


class MicrosoftApp:
    """This class allows you to authenticate Microsoft users to Minecraft"""
    
    def __init__(self, client: msal.ClientApplication, redirect_uri: str):
        self.__client = client
        self.__redirect_uri = redirect_uri

    def authorization_url(self, redirect_uri: str = None) -> str:
        """Returns the authorization url for Microsfot OAuth"""
        return self.__client.get_authorization_request_url(scopes=_DEFAULT_SCOPES, redirect_uri=(redirect_uri or self.__redirect_uri))

    def authenticate(self, auth_code: str, redirect_uri: str = None) -> 'UserSession':
        """Authenticate a user with the auth code
        
        Args:
            auth_code (str): The auth code from the redirect
            redirect_uri (str, optional): The redirect uri for your app

        Returns:
            An instance of UserSession
        """
        response = self.__client.acquire_token_by_authorization_code(auth_code, scopes=_DEFAULT_SCOPES, redirect_uri=(redirect_uri or self.__redirect_uri))
        if response.get('error', False):
            raise MicrosoftInvalidGrant(*response.values())

        xbl_token, userhash = microsoft.authenticate_xbl(response['access_token'])
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        access_token = microsoft.authenticate_minecraft(userhash, xsts_token)

        if not session.owns_minecraft(access_token):
            raise MicrosoftUserNotOwner()

        return UserSession(access_token, response['refresh_token'], True, self._refresh_session, None)
    
    def _refresh_session(self, access_token: str, refresh_token: str):
        response = self.__client.acquire_token_by_refresh_token(refresh_token, _DEFAULT_SCOPES)
        xbl_token, userhash = microsoft.authenticate_xbl(response['access_token'])
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        mc_token = microsoft.authenticate_minecraft(userhash, xsts_token)
        
        return mc_token, response['refresh_token']
