from .api import base
from .api.auth import yggdrasil
from .profile import UserProfile
from .session import UserSession

from .api.files.versions import MinecraftVersions

# Basic api
api_status = base.api_status
name_history = base.name_history

def get_uuid(username: str) -> str:
    """Get uuid of username

    Args:
        username (str): The username which you want the uuid of
    
    Returns:
        The uuid of the username
    """
    return base.get_uuid(username)

def get_uuids(usernames: list) -> list:
    """Get uuid of multiple username

    Note: Limited Endpoint
        The Mojang API only allow 10 usernames maximum, if more than 10 usernames are
        given to the function, multiple request will be made.

    Args:
        usernames (list): The list of username which you want the uuid of
    
    Returns:
        A list of uuid
    """
    return base.get_uuids(usernames)

def get_username(uuid: str) -> str:
    """Get the username of a uuid

    Args:
        uuid (str): The uuid you want the username of

    Returns:
        The username of the uuid
    """
    profile = base.get_profile(uuid)
    if profile:
        return profile['name']


# Connect
def connect(username: str, password: str, client_token: str = None) -> 'UserSession':
    """Connect a user with name and password

    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password
        client_token (str, optional): The client token to use in the authentication (default to None)

    Returns:
        A `UserSession` object
    """
    auth_data = yggdrasil.authenticate_user(username, password, client_token=client_token)
    return UserSession(auth_data['access_token'], auth_data['client_token'])


# Complete profile
def user(username: str = None, uuid: str = None) -> 'UserProfile':
    """Fetch the complete profile by `uuid` or `username`. If both are given 
    the `username` is used

    Args:
        username (str, optional): The username to fetch the profile for
        uuid (str, optional): The uuid to fetch the profile for
    
    Returns:
        A UserProfile object
    """
    if username is not None:
        user_data = base.get_uuid(username, only_uuid=False)
        if user_data:
            user_profile = base.get_profile(user_data['uuid'])
            names = base.name_history(user_data['uuid'])

            return UserProfile.create(**{**user_data, **user_profile, 'names': names})
    elif uuid is not None:
        user_profile = base.get_profile(uuid)
        if user_profile:
            user_data = base.get_uuid(user_profile['name'], only_uuid=False)
            names = base.name_history(user_profile['uuid'])

            return UserProfile.create(**{**user_data, **user_profile, 'names': names})
    else:
        raise Exception('You must at least provide one argument: `username` or `uuid`')


# Minecraft Versions
mcversions = MinecraftVersions()
