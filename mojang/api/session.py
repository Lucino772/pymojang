import datetime as dt

import requests

from ..error.exceptions import *
from ..utils import web
from ..utils.skin import Skin
from .urls import (CHANGE_NAME, CHECK_NAME_CHANGE, GET_PROFILE, RESET_SKIN, UPLOAD_SKIN)


def get_user_name_change(access_token: str) -> dict:
    """Return if user can change name and when it was created

    Args:
        access_token (str): The session's access token

    Returns:
        A dict with the following keys: `created_at` and `name_change_allowed`

    Raises:
        Unauthorized: If the access token is invalid
    """
    data = web.auth_request('get', CHECK_NAME_CHANGE, access_token, exceptions=(PayloadError, Unauthorized))
    return {
        'created_at': dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
        'name_change_allowed': data['nameChangeAllowed']
    }

def change_user_name(access_token: str, name: str):
    """Change the user name

    Args:
        access_token (str): The session's access token
        name (str): The new user name
    
    Raises:
        Unauthorized: If the access token is invalid
        InvalidName: If the new user name is invalid
        UnavailableName: If the new user name is unavailable
    """
    web.auth_request('put', CHANGE_NAME.format(name=name), access_token, exceptions=(InvalidName, UnavailableName, Unauthorized))

def change_user_skin(access_token: str, path: str, variant='classic'):
    """Change user skin

    Args:
        access_token (str): The session's access token
        path (str): The the path to the new skin, either local or remote
        variant (str, optional): The skin variant, either `classic` or `slim`

    Raises:
        Unauthorized: If the access token is invalid
    """
    skin = Skin(path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', (f'image.{skin.extention}', skin.data, f'image/{skin.extention}'))
    ]
    web.auth_request('post', UPLOAD_SKIN, access_token, exceptions=(PayloadError, Unauthorized), files=files, headers={'content-type': None})

def reset_user_skin(access_token: str, uuid: str):
    """Reset user skin

    Args:
        access_token (str): The session's access token
        uuid (str): The user uuid

    Raises:
        Unauthorized: If the access token is invalid
    """
    web.auth_request('delete', RESET_SKIN.format(uuid=uuid), access_token, exceptions=(PayloadError, Unauthorized))
