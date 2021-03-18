import requests
from . import api
from .session import UserSession
from .profile import UserProfile

def user(username=None, password=None):
    sess = requests.Session()
    if isinstance(username, str) and isinstance(password, str):
        us = UserSession(sess)
        us.connect(username, password)
        
        return us
    elif isinstance(username, str):
        uuid_data = api.uuid(username, only_uuid=False)
        names = api.names(uuid_data['uuid'])
        name_change_data = api.user.check_name_change()
        profile_data = api.user.get_profile(uuid=uuid_data['uuid'])

        data = {'names': names, **uuid_data, **profile_data, **name_change_data}

        return UserProfile(**data)

