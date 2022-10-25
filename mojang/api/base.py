import base64
import datetime as dt
import json
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import requests

from ..exceptions import InvalidName
from . import helpers, urls
from .models import Cape, Skin
from .structures import ServiceStatus, UnauthenticatedProfile


def get_status() -> List[ServiceStatus]:
    """Get the status of Mojang's services

    :Example:

    >>> import mojang
    >>> mojang.get_status()
    [
        ServiceStatus(name='minecraft.net', status='green'),
        ServiceStatus(name='session.minecraft.net', status='green'),
        ServiceStatus(name='account.mojang.com', status='green'),
        ServiceStatus(name='authserver.mojang.com', status='green'),
        ServiceStatus(name='sessionserver.mojang.com', status='red'),
        ServiceStatus(name='api.mojang.com', status='green'),
        ServiceStatus(name='textures.minecraft.net', status='green'),
        ServiceStatus(name='mojang.com', status='green')
    ]

    """
    _status = [
        ServiceStatus(name="minecraft.net", status="unknown"),
        ServiceStatus(name="session.minecraft.net", status="unknown"),
        ServiceStatus(name="account.mojang.com", status="unknown"),
        ServiceStatus(name="authserver.mojang.com", status="unknown"),
        ServiceStatus(name="sessionserver.mojang.com", status="unknown"),
        ServiceStatus(name="api.mojang.com", status="unknown"),
        ServiceStatus(name="textures.minecraft.net", status="unknown"),
        ServiceStatus(name="mojang.com", status="unknown"),
    ]

    return _status


def get_blocked_servers() -> List[str]:
    """Get a list of blocked servers hashes"""
    response = requests.get(urls.api_get_blocked_servers)
    _, data = helpers.err_check(response)

    return data.split("\n")


def get_uuid(username: str) -> Optional[str]:
    """Get uuid for a username

    :param str username: The username you want the uuid of

    :Example:

    >>> import mojang
    >>> mojang.get_uuid('Notch')
    '069a79f444e94726a5befca90e38aaf5'
    """
    if len(username) == 0 or len(username) > 16:
        raise InvalidName()

    response = requests.get(urls.api_get_uuid(username))
    code, data = helpers.err_check(response)

    if code == 204:
        return None

    return data["id"]


def get_uuids(usernames: Iterable[str]) -> Dict[str, Optional[str]]:
    """Get uuids for multiple usernames

    .. admonition:: Limited Endpoint
        :class: note

        The Mojang API only allow 10 usernames maximum, if more than 10 usernames are
        given to the function, multiple request will be made.

    :param list usernames: The usernames you want the uuid of

    :Example:

    >>> import mojang
    >>> mojang.get_uuids(['Notch', '_jeb'])
    {
        'notch': '069a79f444e94726a5befca90e38aaf5',
        '_jeb': '45f50155c09f4fdcb5cee30af2ebd1f0'
    }
    """
    usernames = [u.lower() for u in usernames]
    ret = dict.fromkeys(usernames, None)

    # Check for invalid names
    if any([not (0 < len(u) <= 16) for u in usernames]):
        raise InvalidName()

    for i in range(0, len(usernames), 10):
        response = requests.post(
            urls.api_get_uuids, json=usernames[i : i + 10]
        )
        _, data = helpers.err_check(response)

        for item in data:
            ret[item["name"].lower()] = item["id"]

    return ret


def get_username(uuid: str) -> Optional[str]:
    """Get username for a uuid

    :param uuid str: The uuid you want the username of

    :Example:

    >>> import mojang
    >>> mojang.get_username('069a79f444e94726a5befca90e38aaf5')
    'Notch'
    """
    response = requests.get(urls.api_get_username(uuid))
    code, data = helpers.err_check(response, (400, ValueError))

    if code == 204:
        return None

    return data["name"]


def get_profile(uuid: str) -> Optional[UnauthenticatedProfile]:
    """Returns the full profile of a user

    :param str uuid: The uuid of the profile

    :Example:

    >>> import mojang
    >>> mojang.get_profile('069a79f444e94726a5befca90e38aaf5')
    UnauthenticatedProfile(
        name='Notch',
        uuid='069a79f444e94726a5befca90e38aaf5',
        is_legacy=False,
        is_demo=False,
        skin=Skin(source='...', variant='classic'),
        cape=None
    )
    """
    response = requests.get(urls.api_user_profile(uuid))
    code, data = helpers.err_check(response, (400, ValueError))

    if code == 204:
        return None

    # Load skin and cape
    textures_data = json.loads(
        base64.b64decode(data["properties"][0]["value"])
    )

    skin = None
    skin_data = textures_data["textures"].get("SKIN", None)
    if skin_data is not None:
        skin = Skin(
            skin_data["url"],
            skin_data.get("metadata", {"model": "classic"})["model"],
        )

    cape = None
    cape_data = textures_data["textures"].get("CAPE", None)
    if cape_data is not None:
        cape = Cape(cape_data["url"])

    return UnauthenticatedProfile(
        name=data["name"],
        uuid=uuid,
        is_legacy=data.get("legacy", False),
        is_demo=data.get("demo", False),
        skin=skin,
        cape=cape,
    )
