import msal

from .models import MojangAuthenticationApp


def app(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
) -> "MojangAuthenticationApp":
    client = msal.ClientApplication(
        client_id,
        client_credential=client_secret,
        authority="https://login.microsoftonline.com/consumers",
    )
    return MojangAuthenticationApp(client, redirect_uri)
