from .api import base
from .api.auth import yggdrasil
from .profile import UserProfile
from .session import UserSession

# Basic api
api_status = base.api_status
name_history = base.name_history

def get_uuid(username: str):
    return base.get_uuid(username)

def get_uuids(usernames: list):
    return base.get_uuids(usernames)

def get_username(uuid: str):
    profile = base.get_profile(uuid)
    if profile:
        return profile['name']


# Connect
def connect(username: str, password: str, client_token=None):
    auth_data = yggdrasil.authenticate_user(username, password, client_token=client_token)
    return UserSession(auth_data['access_token'], auth_data['client_token'])


# Complete profile
def user(username: str = None, uuid: str = None):
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


