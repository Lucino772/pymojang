from typing import Optional, Tuple

import requests

from ...exceptions import CredentialsError, MigratedAccount, TokenError
from ..utils import urls, helpers


def authenticate(
    username: str, password: str, client_token: Optional[str] = None
) -> Tuple[str, str]:
    """Authenticate a user with name and password

    Args:
        username (str): The username of email if account is not legacy
        password (str): The user password
        client_token (str, optional): The client token to use (default to None)

    Returns:
        AuthenticationInfo

    Raises:
        CredentialsError: If username and password are invalid
        PayloadError: If credentials are not formated correctly

    Example:

        ```python
        from mojang.account.auth import yggdrasil

        auth_info = yggdrasil.authenticate('USERNAME_OR_EMAIL','PASSWORD')
        print(auth_info)
        ```
        ```
        AuthenticationInfo(access_token='ACCESS_TOKEN', client_token='CLIENT_TOKEN', uuid='...', name='...', legacy=False, demo=False)
        ```
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

    Args:
        access_token (str): The access token to refresh
        client_token (str): The client token used to generate the access token

    Returns:
        AuthenticationInfo

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly

    Example:

        ```python
        from mojang.account.auth import yggdrasil

        refresh_info = yggdrasil.refresh('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
        print(refresh_info)
        ```
        ```
        AuthenticationInfo(access_token='NEW_ACCESS_TOKEN', client_token='CLIENT_TOKEN', uuid='...', name='...', legacy=False, demo=False)
        ```
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

    Args:
        access_token (str): The access token to validate
        client_token (str): The client token used to generate the access token

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly

    Example:

        ```python
        from mojang.account.auth import yggdrasil

        yggdrasil.validate('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
        ```
    """
    payload = {"accessToken": access_token, "clientToken": client_token}
    response = requests.post(urls.api_yggdrasil_validate, json=payload)
    code, _ = helpers.err_check(response, (400, ValueError))
    return code == 204


def signout(username: str, password: str):
    """Signout user with name and password

    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password

    Raises:
        CredentialsError: If username and password are invalid
        PayloadError: If credentials are not formated correctly

    Example:

        ```python
        from mojang.account.auth import yggdrasil

        yggdrasil.signout('USERNAME_OR_EMAIL','PASSWORD')
        ```
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

    Args:
        access_token (str): The access token to invalidate
        client_token (str): The client token used to generate the access token

    Raises:
        TokenError: If client token is not the one used to generate the access token
        PayloadError: If the tokens are not formated correctly

    Example:

        ```python
        from mojang.account.auth import yggdrasil

        yggdrasil.invalidate('CURRENT_ACCESS_TOKEN','CLIENT_TOKEN')
        ```
    """
    payload = {"accessToken": access_token, "clientToken": client_token}
    response = requests.post(urls.api_yggdrasil_invalidate, json=payload)
    code, _ = helpers.err_check(
        response,
        (400, ValueError),
        (403, TokenError),
    )
    return code == 204
