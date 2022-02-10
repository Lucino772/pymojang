from typing import Optional, Tuple

import requests

from ...exceptions import CredentialsError, MigratedAccount, TokenError
from .. import helpers, urls


def authenticate(
    username: str, password: str, client_token: Optional[str] = None
) -> Tuple[str, str]:
    """Authenticate a user with name and password

    :param str username: The username of email if account is not legacy
    :param str password: The user password
    :param client_token: The client token to use
    :type client_token: str or None

    :raises CredentialsError: if username and password are invalid
    :raises PayloadError: if credentials are not formated correctly

    :Example:

    >>> from mojang.account.auth import yggdrasil
    >>> yggdrasil.authenticate('USERNAME_OR_EMAIL','PASSWORD')
    AuthenticationInfo(access_token='ACCESS_TOKEN', client_token='CLIENT_TOKEN', uuid='...', name='...', legacy=False, demo=False)
    """
    payload = {
        "username": username,
        "password": password,
        "clientToken": client_token,
        "agent": {"name": "Minecraft", "version": 1},
    }
    response = requests.post(urls.api_yggdrasil_authenticate, json=payload)
    _, data = helpers.err_check(
        response,
        (400, ValueError),
        ([403, 429], CredentialsError),
        (410, MigratedAccount),
    )

    return data["accessToken"], data["clientToken"]


def refresh(access_token: str, client_token: str) -> Tuple[str, str]:
    """Refresh an invalid access token

    :param str access_token: The access token to refresh
    :param str client_token: The client token used to generate the access token

    :raises TokenError: if client token is not the one used to generate the access token
    :raises PayloadError: if the tokens are not formated correctly

    :Example:

    >>> from mojang.account.auth import yggdrasil
    >>> yggdrasil.refresh('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
    AuthenticationInfo(access_token='NEW_ACCESS_TOKEN', client_token='CLIENT_TOKEN', uuid='...', name='...', legacy=False, demo=False)
    """
    payload = {"accessToken": access_token, "clientToken": client_token}
    response = requests.post(urls.api_yggdrasil_refresh, json=payload)
    _, data = helpers.err_check(
        response,
        (400, ValueError),
        (403, TokenError),
    )

    return data["accessToken"], data["clientToken"]


def validate(access_token: str, client_token: str):
    """Validate an access token

    :param str access_token: The access token to validate
    :param str client_token: The client token used to generate the access token

    :raises TokenError: if client token is not the one used to generate the access token
    :raises PayloadError: if the tokens are not formated correctly

    :Example:

    >>> from mojang.account.auth import yggdrasil
    >>> yggdrasil.validate('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
    """
    payload = {"accessToken": access_token, "clientToken": client_token}
    response = requests.post(urls.api_yggdrasil_validate, json=payload)
    code, _ = helpers.err_check(response, (400, ValueError))
    return code == 204


def signout(username: str, password: str):
    """Signout user with name and password

    :param str username: The username of email if account is not legacy
    :param str password: The user password

    :raises CredentialsError: if username and password are invalid
    :raises PayloadError: if credentials are not formated correctly

    :Example:

    >>> from mojang.account.auth import yggdrasil
    >>> yggdrasil.signout('USERNAME_OR_EMAIL','PASSWORD')
    """
    payload = {"username": username, "password": password}
    response = requests.post(urls.api_yggdrasil_signout, json=payload)
    code, _ = helpers.err_check(
        response,
        (400, ValueError),
        ([403, 429], CredentialsError),
    )
    return code == 204


def invalidate(access_token: str, client_token: str):
    """Invalidate an access token

    :param str access_token: The access token to invalidate
    :param str client_token: The client token used to generate the access token

    :raises TokenError: if client token is not the one used to generate the access token
    :raises PayloadError: if the tokens are not formated correctly

    :Example:

    >>> from mojang.account.auth import yggdrasil
    >>> yggdrasil.invalidate('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
    """
    payload = {"accessToken": access_token, "clientToken": client_token}
    response = requests.post(urls.api_yggdrasil_invalidate, json=payload)
    code, _ = helpers.err_check(
        response,
        (400, ValueError),
        (403, TokenError),
    )
    return code == 204
