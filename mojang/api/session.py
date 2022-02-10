import datetime as dt

import jwt
import requests

from ..exceptions import (
    InvalidName,
    NotCapeOwner,
    Unauthorized,
    UnavailableName,
)
from . import helpers, urls
from .base import get_names
from .structures.profile import AuthenticatedUserProfile
from .structures.session import Cape, NameChange, Skin


def get_user_name_change(access_token: str) -> NameChange:
    """Return if user can change name and when it was created

    :param str access_token: The session access token

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.get_username_change('ACCESS_TOKEN')
    NameChange(allowed=True, created_at=datetime.datetime(2006, 4, 29, 10, 10, 10))
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.get(urls.api_session_name_change, headers=headers)
    _, data = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )

    data["created_at"] = dt.datetime.strptime(
        data.pop("createdAt"), "%Y-%m-%dT%H:%M:%SZ"
    )
    data["allowed"] = data.pop("nameChangeAllowed")

    return NameChange(allowed=data["allowed"], created_at=data["created_at"])


def change_user_name(access_token: str, name: str):
    """Change name of authenticated user

    :param str access_token: The session access token
    :param str name: The new user name

    :raises Unauthorized: if the access token is invalid
    :raises InvalidName: if the new user name is invalid
    :raises UnavailableName: if the new user name is unavailable

    :Example:

    >>> from mojang.account import session
    >>> session.change_user_name('ACCESS_NAME', 'NEW_NAME')
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.put(
        urls.api_session_change_name(name), headers=headers
    )
    code, _ = helpers.err_check(
        response,
        (400, InvalidName),
        (403, UnavailableName),
        (401, Unauthorized),
    )
    return code == 200


def change_user_skin(access_token: str, path: str, variant="classic"):
    """Change skin of authenticated user

    :param str access_token: The session access token
    :param str path: The the path to the new skin, either local or remote
    :parama str variant: The skin variant, either `classic` or `slim`

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.change_user_skin('ACCESS_TOKEN', 'http://...')
    """
    skin = Skin(source=path, variant=variant)
    files = [
        ("variant", skin.variant),
        ("file", ("image.png", skin.data, "image/png")),
    ]
    headers = helpers.get_headers(bearer=access_token)
    headers["content-type"] = None
    response = requests.post(
        urls.api_session_change_skin, headers=headers, files=files
    )
    code, _ = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )
    return code == 204


def reset_user_skin(access_token: str):
    """Reset skin of authenticated user

    :param str access_token: The session access token

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.reset_user_skin('ACCESS_TOKEN', 'USER_UUID')
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.delete(urls.api_session_reset_skin, headers=headers)
    code, _ = helpers.err_check(
        response, (400, ValueError), (401, Unauthorized)
    )
    return code == 200


def show_user_cape(access_token: str, cape_id: str):
    """Show user cape

    :param str access_token: The session access token

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.show_user_cape('ACCESS_TOKEN')
    """
    payload = {"capeId": cape_id}
    headers = helpers.get_headers(bearer=access_token)
    response = requests.put(
        urls.api_session_cape_visibility, headers=headers, json=payload
    )
    code, _ = helpers.err_check(
        response, (400, NotCapeOwner), (401, Unauthorized)
    )
    return code == 200


def hide_user_cape(access_token: str):
    """Hide user cape

    :param str access_token: The session access token

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.hide_user_cape('ACCESS_TOKEN')
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.delete(
        urls.api_session_cape_visibility, headers=headers
    )
    code, _ = helpers.err_check(response, (401, Unauthorized))
    return code == 200


def owns_minecraft(
    access_token: str, verify_sig: bool = False, public_key: str = None
) -> bool:
    """Returns True if the authenticated user owns minecraft

    :param str access_token: The session access token
    :param str verify_sig: If True, will check the jwt sig with the public key
    :param str public_key: The key to use to verify jwt sig

    :raises Unauthorized: if the access token is invalid

    :Example:

    >>> from mojang.account import session
    >>> session.owns_minecraft('ACCESS_TOKEN')
    True
    """
    headers = helpers.get_headers(bearer=access_token)
    response = requests.get(urls.api_session_ownership, headers=headers)
    _, data = helpers.err_check(response, (401, Unauthorized))

    if verify_sig:
        for i in data.get("items", []):
            jwt.decode(i["signature"], public_key, algorithms=["RS256"])

        jwt.decode(data["signature"], public_key, algorithms=["RS256"])

    return not len(data["items"]) == 0


def get_profile(access_token: str) -> AuthenticatedUserProfile:
    """Returns the full profile of a authenticated user

    :param str access_token: The session access token

    :raises Unauthorized: if the access token is invalid
    """

    headers = helpers.get_headers(bearer=access_token)
    response = requests.get(urls.api_session_profile, headers=headers)
    _, data = helpers.err_check(response, (401, Unauthorized))

    skins = []
    for item in data["skins"]:
        skins.append(
            Skin(
                item["url"],
                item["variant"],
                id=item["id"],
                state=item["state"],
            )
        )

    capes = []
    for item in data["capes"]:
        capes.append(
            Cape(
                item["url"],
                id=item["id"],
                state=item["state"],
            )
        )

    return AuthenticatedUserProfile(
        name=data["name"],
        uuid=data["id"],
        is_legacy=False,
        is_demo=False,
        names=get_names(data["id"]),
        skins=skins,
        capes=capes,
    )
