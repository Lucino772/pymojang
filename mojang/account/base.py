import base64
import datetime as dt
import json
from typing import List

import requests

from ..exceptions import InvalidName
from .structures.base import (
    NameInfo,
    NameInfoList,
    ServiceStatus,
    StatusCheck,
    UUIDInfo,
)
from .structures.profile import UnauthenticatedProfile
from .structures.session import Cape, Skin
from .utils import urls, helpers


def status() -> StatusCheck:
    """Get the status of Mojang's services

    Returns:
        StatusCheck

    Example:

        Get status for all services
        ```python
        import mojang

        status = mojang.status()
        print(status)
        ```
        ```bash
        (
            ServiceStatus(name='minecraft.net', status='green'),
            ServiceStatus(name='session.minecraft.net', status='green'),
            ServiceStatus(name='account.mojang.com', status='green'),
            ServiceStatus(name='authserver.mojang.com', status='green'),
            ServiceStatus(name='sessionserver.mojang.com', status='red'),
            ServiceStatus(name='api.mojang.com', status='green'),
            ServiceStatus(name='textures.minecraft.net', status='green'),
            ServiceStatus(name='mojang.com', status='green')
        )
        ```

        Get status for one specific service
        ```python
        import mojang

        status = mojang.status().get('minecraft.net')
        print(status)
        ```
        ```bash
        ServiceStatus(name='minecraft.net', status='green')
        ```
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

    return StatusCheck(_status)


def get_uuid(username: str) -> UUIDInfo:
    """Get uuid of username

    Args:
        username (str): The username which you want the uuid of

    Returns:
        UUIDInfo

    Example:

        ```python
        import mojang
        uuid_info = mojang.get_uuid('Notch')
        print(uuid_info)
        ```
        ```
        UUIDInfo(name='Notch', uuid='069a79f444e94726a5befca90e38aaf5', legacy=False, demo=False)
        ```
    """
    if len(username) == 0 or len(username) > 16:
        raise InvalidName()

    response = requests.get(urls.api_get_uuid(username))
    code, data = helpers.err_check(response)

    if code == 204:
        return None

    return UUIDInfo(
        name=data["name"],
        uuid=data["id"],
        legacy=data.get("legacy", False),
        demo=data.get("demo", False),
    )


def get_uuids(usernames: list) -> List["UUIDInfo"]:
    """Get uuid of multiple username

    Note: Limited Endpoint
        The Mojang API only allow 10 usernames maximum, if more than 10 usernames are
        given to the function, multiple request will be made.

    Args:
        usernames (list): The list of username which you want the uuid of

    Returns:
        A list of UUIDInfo

    Example:

        ```python
        import mojang
        uuids_info = mojang.get_uuids(['Notch', '_jeb'])
        print(uuids_info)
        ```
        ```
        [
            UUIDInfo(name='Notch', uuid='069a79f444e94726a5befca90e38aaf5', legacy=False, demo=False),
            UUIDInfo(name='_jeb', uuid='45f50155c09f4fdcb5cee30af2ebd1f0', legacy=False, demo=False)
        ]
        ```
    """
    usernames = list(map(lambda u: u.lower(), usernames))
    _uuids = [None] * len(usernames)

    # Check for invalid names
    valid_usernames = list(filter(lambda u: 0 < len(u) <= 16, usernames))
    if len(valid_usernames) < len(usernames):
        raise InvalidName()

    for i in range(0, len(valid_usernames), 10):
        response = requests.post(
            urls.api_get_uuids, json=valid_usernames[i : i + 10]
        )
        _, data = helpers.err_check(response)

        for item in data:
            index = usernames.index(item["name"].lower())
            item["uuid"] = item.pop("id")
            _uuids[index] = UUIDInfo(**item)

    return _uuids


def names(uuid: str) -> NameInfoList:
    """Get the user's name history

    Args:
        uuid (str): The user's uuid

    Returns:
        NameInfoList

    Example:

        ```python
        import mojang

        name_history = mojang.names('65a8dd127668422e99c2383a07656f7a')
        print(name_history)
        ```
        ```
        (
            NameInfo(name='piewdipie', changed_to_at=None),
            NameInfo(name='KOtMotros', changed_to_at=datetime.datetime(2020, 3, 4, 17, 45, 26))
        )
        ```
    """
    response = requests.get(urls.api_name_history(uuid))
    code, data = helpers.err_check(response, (400, ValueError))

    if code == 204:
        return None

    _names = []
    for item in data:
        changed_to_at = None
        if "changedToAt" in item.keys():
            changed_to_at = dt.datetime.fromtimestamp(
                item["changedToAt"] / 1000
            )
        _names.append(NameInfo(name=item["name"], changed_to_at=changed_to_at))

    return NameInfoList(_names)


def user(uuid: str) -> UnauthenticatedProfile:
    """Returns the full profile of a user

    Args:
        uuid (str): The uuid of the profile

    Returns:
        UnauthenticatedProfile

    Example:

        ```python
        import mojang

        profile = mojang.user('069a79f444e94726a5befca90e38aaf5')
        print(profile)
        ```
        ```
        UnauthenticatedProfile(
            name='Notch',
            uuid='069a79f444e94726a5befca90e38aaf5',
            is_legacy=False,
            is_demo=False,
            names=(NameInfo(name='Notch', changed_to_at=None),),
            skin=Skin(source='...', variant='classic'),
            cape=None
        )
        ```
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
    if skin_data:
        skin = Skin(
            skin_data["url"],
            skin_data.get("metadata", {"model": "classic"})["model"],
        )

    cape = None
    cape_data = textures_data["textures"].get("CAPE", None)
    if cape_data:
        cape = Cape(cape_data["url"])

    return UnauthenticatedProfile(
        name=data["name"],
        uuid=uuid,
        is_legacy=data.get("legacy", False),
        is_demo=data.get("demo", False),
        names=names(uuid),
        skin=skin,
        cape=cape,
    )
