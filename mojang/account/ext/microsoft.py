import msal
from ..auth import microsoft
from .session import UserSession


_DEFAULT_SCOPES = ['XboxLive.signin']

def microsoft_app(client_id: str, client_secret: str, redirect_uri: str = 'http://example.com'):
    client = msal.ClientApplication(client_id, client_credential=client_secret, authority='https://login.microsoftonline.com/consumers')
    return MicrosoftApp(client, redirect_uri)


class MicrosoftApp:
    
    def __init__(self, client: msal.ClientApplication, redirect_uri: str):
        self.__client = client
        self.__redirect_uri = redirect_uri

    def authorization_url(self, redirect_uri: str = None) -> str:
        return self.__client.get_authorization_request_url(scopes=_DEFAULT_SCOPES, redirect_uri=(redirect_uri or self.__redirect_uri))

    def authenticate(self, auth_code: str, redirect_uri: str = None) -> 'UserSession':
        response = self.__client.acquire_token_by_authorization_code(auth_code, scopes=_DEFAULT_SCOPES, redirect_uri=(redirect_uri or self.__redirect_uri))
        xbl_token, userhash = microsoft.authenticate_xbl(response['access_token'])
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        access_token = microsoft.authenticate_minecraft(userhash, xsts_token)

        return UserSession(access_token, response['refresh_token'], True, self._refresh_session, None)
    
    def _refresh_session(self, access_token: str, refresh_token: str):
        response = self.__client.acquire_token_by_refresh_token(refresh_token, _DEFAULT_SCOPES)
        xbl_token, userhash = microsoft.authenticate_xbl(response['access_token'])
        xsts_token, userhash = microsoft.authenticate_xsts(xbl_token)
        mc_token = microsoft.authenticate_minecraft(userhash, xsts_token)
        
        return mc_token, response['refresh_token']
