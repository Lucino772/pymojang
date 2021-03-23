import datetime as dt

import requests

from ..error.exceptions import *
from ..utils import web
from ..utils.skin import Skin
from .urls import (CHANGE_NAME, CHECK_NAME_CHANGE, GET_PROFILE, RESET_SKIN,
                   UPLOAD_SKIN)


def get_user_name_change(access_token: str) -> dict:
    data = web.auth_request('get', CHECK_NAME_CHANGE, access_token, exceptions=(PayloadError, Unauthorized))
    return {
        'created_at': dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
        'name_change_allowed': data['nameChangeAllowed']
    }

def change_user_name(access_token: str, name: str):
    web.auth_request('put', CHANGE_NAME.format(name=name), access_token, exceptions=(InvalidName, UnavailableName, Unauthorized))

def change_user_skin(access_token: str, path: str, variant='classic'):
    skin = Skin(path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', (f'image.{skin.extention}', skin.data, f'image/{skin.extention}'))
    ]
    web.auth_request('post', UPLOAD_SKIN, access_token, exceptions=(PayloadError, Unauthorized), files=files, headers={'content-type': None})

def reset_user_skin(access_token: str, uuid: str):
    web.auth_request('delete', RESET_SKIN.format(uuid=uuid), access_token, exceptions=(PayloadError, Unauthorized))
