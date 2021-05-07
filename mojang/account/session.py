import datetime as dt

import requests

from ..exceptions import *
from .structures.session import NameChange, Skin
from .utils.auth import BearerAuth
from .utils.urls import URLs


def get_user_name_change(access_token: str) -> NameChange:
    """Return if user can change name and when it was created
    
    Args:
        access_token (str): The session's access token
    
    Returns:
        NameChange
    
    Raises:
        Unauthorized: If the access token is invalid
    """
    response = requests.get(URLs.name_change(), auth=BearerAuth(access_token))
    data = handle_response(response, PayloadError, Unauthorized)

    data['created_at'] = dt.datetime.strptime(data.pop('createdAt'), '%Y-%m-%dT%H:%M:%SZ')
    data['allowed'] = data.pop('nameChangeAllowed')

    return NameChange(**data)

def change_user_name(access_token: str, name: str):
    """Change name of authenticated user
    
    Args:
        access_token (str): The session's access token
        name (str): The new user name
    
    Raises:
        Unauthorized: If the access token is invalid
        InvalidName: If the new user name is invalid
        UnavailableName: If the new user name is unavailable
    """
    response = requests.put(URLs.change_name(name), auth=BearerAuth(access_token))
    handle_response(response, InvalidName, UnavailableName, Unauthorized)

def change_user_skin(access_token: str, path: str, variant='classic'):
    """Change skin of authenticated user
    
    Args:
        access_token (str): The session's access token
        path (str): The the path to the new skin, either local or remote
        variant (str, optional): The skin variant, either `classic` or `slim`
    
    Raises:
        Unauthorized: If the access token is invalid
    """
    skin = Skin(source=path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', ('image.png', skin.data, f'image/png'))
    ]
    response = requests.post(URLs.change_skin(), auth=BearerAuth(access_token), files=files, headers={'content-type': None})
    handle_response(response, PayloadError, Unauthorized)

def reset_user_skin(access_token: str, uuid: str):
    """Reset skin of authenticated user
    
    Args:
        access_token (str): The session's access token
        uuid (str): The user uuid
    
    Raises:
        Unauthorized: If the access token is invalid
    """
    response = requests.delete(URLs.reset_skin(uuid), auth=BearerAuth(access_token))
    handle_response(response, PayloadError, Unauthorized)
