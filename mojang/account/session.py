import requests
import datetime as dt

from ._urls import URLs
from ._structures import NameChange, Skin
from ._auth import BearerAuth

# TODO: Handle errors and exception

def get_user_name_change(access_token: str):
    response = requests.get(URLs.name_change(), auth=BearerAuth(access_token))

    data = response.json()
    data['created_at'] = dt.datetime.strptime(data.pop('createdAt'), '%Y-%m-%dT%H:%M:%SZ')
    data['allowed'] = data.pop('nameChangeAllowed')

    return NameChange(**data)

def change_user_name(access_token: str, name: str):
    response = requests.put(URLs.change_name(name), auth=BearerAuth(access_token))

def change_user_skin(access_token: str, path: str, variant='classic'):
    skin = Skin(source=path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', ('image.png', skin.data, f'image/png'))
    ]
    response = requests.post(URLs.change_skin(), auth=BearerAuth(access_token), files=files, headers={'content-type': None})

def reset_user_skin(access_token: str, uuid: str):
    response = requests.delete(URLs.reset_skin(uuid), auth=BearerAuth(access_token))
