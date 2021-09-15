import datetime as dt

import jwt
import requests

from ..exceptions import *
from .structures.session import NameChange, Skin, Cape
from .structures.base import UserProfile
from .utils.auth import BearerAuth
from .utils.urls import URLs
from .base import names


def get_user_name_change(access_token: str) -> NameChange:
    """Return if user can change name and when it was created
    
    Args:
        access_token (str): The session's access token
    
    Returns:
        NameChange
    
    Raises:
        Unauthorized: If the access token is invalid

    Example:

        ```python
        from mojang.account import session

        name_change = session.get_user_name_change('ACCESS_TOKEN')
        print(name_change)
        ```
        ```bash
        NameChange(allowed=True, created_at=datetime.datetime(2006, 4, 29, 10, 10, 10))
        ```
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
    
    Example:

        ```python
        from mojang.account import session

        session.change_user_name('ACCESS_TOKEN', 'my_super_cool_name')
        ```
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

    Example:

        ```python
        from mojang.account import session

        session.change_user_skin('ACCESS_TOKEN', 'http://...')
        ```
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

    Example:

        ```python
        from mojang.account import session

        session.reset_user_skin('ACCESS_TOKEN', 'USER_UUID')
        ```
    """
    response = requests.delete(URLs.reset_skin(uuid), auth=BearerAuth(access_token))
    handle_response(response, PayloadError, Unauthorized)

def owns_minecraft(access_token: str, verify_sig: bool = False, public_key: str = None) -> bool:
    """Returns True if the authenticated user owns minecraft
    
    Args:
        access_token (str): The session's access token
        verify_sig (bool, optional): If True, will check the jwt sig with the public key
        public_key (str, optional): The key to use to verify jwt sig 

    Returns:
        True if user owns the game, else False

    Raises:
        Unauthorized: If the access token is invalid

    Example:

        ```python
        from mojang.account import session

        if session.owns_minecraft('ACCESS_TOKEN'):
            print('This user owns minecraft')
        ```
    """
    response = requests.get(URLs.check_minecraft_onwership(), auth=BearerAuth(access_token))
    data = handle_response(response, Unauthorized)
    
    if verify_sig:
        for i in data.get('items', []):
            jwt.decode(i['signature'], public_key, algorithms=['RS256'])

        jwt.decode(data['signature'], public_key, algorithms=['RS256'])

    return not len(data['items']) == 0

def get_profile(access_token: str):
    response = requests.get(URLs.get_profile(), auth=BearerAuth(access_token))
    data = handle_response(response, Unauthorized)

    _dict = dict.fromkeys(UserProfile._fields, None)

    _dict['name'] = data['name']
    _dict['uuid'] = data['id']
    _dict['names'] = names(data['id'])

    if len(data['skins']) > 0:
        _dict['skin'] = Skin(data['skins'][0]['url'], data['skins'][0]['variant'])
    
    if len(data['capes']) > 0:
        _dict['cape'] = Cape(data['capes'][0]['url'])

    _dict['is_legacy'] = False
    _dict['is_demo'] = False
    
    return UserProfile(**_dict)
