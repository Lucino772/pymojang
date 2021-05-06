import datetime as dt

import requests

from ..exceptions import *
from ._auth import BearerAuth
from ._structures import NameChange, Skin
from ._urls import URLs


def get_user_name_change(access_token: str):
    response = requests.get(URLs.name_change(), auth=BearerAuth(access_token))
    data = handle_response(response, PayloadError, Unauthorized)

    data['created_at'] = dt.datetime.strptime(data.pop('createdAt'), '%Y-%m-%dT%H:%M:%SZ')
    data['allowed'] = data.pop('nameChangeAllowed')

    return NameChange(**data)

def change_user_name(access_token: str, name: str):
    response = requests.put(URLs.change_name(name), auth=BearerAuth(access_token))
    handle_response(response, InvalidName, UnavailableName, Unauthorized)

def change_user_skin(access_token: str, path: str, variant='classic'):
    skin = Skin(source=path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', ('image.png', skin.data, f'image/png'))
    ]
    response = requests.post(URLs.change_skin(), auth=BearerAuth(access_token), files=files, headers={'content-type': None})
    handle_response(response, PayloadError, Unauthorized)

def reset_user_skin(access_token: str, uuid: str):
    response = requests.delete(URLs.reset_skin(uuid), auth=BearerAuth(access_token))
    handle_response(response, PayloadError, Unauthorized)
