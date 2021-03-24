"""
Functions for the basic MojangAPI
"""
import datetime as dt
import json
from base64 import urlsafe_b64decode

from ..error.exceptions import PayloadError
from ..utils import web
from ..utils.cape import Cape
from ..utils.skin import Skin
from .urls import GET_PROFILE, GET_UUID, GET_UUIDS, NAME_HISTORY, STATUS_CHECK


def api_status(service: str = None) -> dict:
    """Get the status of Mojang's services

    Args:
        service (str, optional): The name of the service which you want to know the status

    Returns:
        If service is given, return only the status for this service else return a dict
        with all the status for each services
    """
    res = {}
    
    data = web.request('get', STATUS_CHECK)
    for s in data:
        res.update(s)

    if service:
        return res[service]
    
    return res

def name_history(uuid: str) -> list:
    """Get the user's name history

    Args:
        uuid (str): The user's uuid
    
    Returns:
        A list of tuples, each containing the name and the datetime at which it was
        changed to
    """
    names = []

    data = web.request('get', NAME_HISTORY.format(uuid=uuid))
    for item in data:
        changed_at = None
        if 'changedToAt' in item.keys():
            changed_at = dt.datetime.fromtimestamp(item['changedToAt'] / 1000)
        names.append((item['name'], changed_at))
    
    return names

def get_uuid(username: str, only_uuid: bool = True) -> dict:
    """Get uuid of username

    Args:
        username (str): The username which you want the uuid of
        only_uuid (bool): If True only the uuid is returned (default True)
    
    Returns:
        If only_uuid is True, then only the uuid of the username is returned. 
        If not, a dict is returned with the following keys: `name`, `uuid`, 
        `legacy` and `demo`.
    """
    data = web.request('get', GET_UUID.format(name=username))
    
    if data:
        data['uuid'] = data.pop('id')
        data['legacy'] = data.get('legacy', False)
        data['demo'] = data.get('demo', False)

        if only_uuid:
            return data['uuid']
    else:
        data = None

    return data
    
def get_uuids(usernames: list, only_uuid: bool = True) -> list:
    """Get uuid of username

    Note: Limited Endpoint
        The Mojang API only allow 10 usernames maximum, if more than 10 usernames are
        given to the function, multiple request will be made.

    Args:
        usernames (list): The list of username which you want the uuid of
        only_uuid (bool): If True only the uuid is returned for each username (default True)
    
    Returns:
        If only_uuid is True, then a list of uuid is returned. If not, a list of dict is returned. 
        Each dict contains the following keys: `name`, `uuid`, `legacy` and `demo`.
    """
    res = [None]*len(usernames)

    for i in range(0, len(usernames), 10):
        data = web.request('post', GET_UUIDS, exceptions=(PayloadError,),json=usernames[i:i+10])
        for item in data:
            index = usernames.index(item['name'])
            if not only_uuid:
                res[index] = {
                    'uuid': item['id'],
                    'name': item['name'], 
                    'legacy': item.get('legacy',False),
                    'demo': item.get('demo', False)
                }
            else:
                res[index] = item['id']

    return res

def get_profile(uuid: str) -> dict:
    """Get profile information by uuid

    Args:
        uuid (str): The uuid of the profile
    
    Returns:
        A dict with the following keys: `uuid`, `name`, `skins` and `capes`
    """
    data = web.request('get', GET_PROFILE.format(uuid=uuid), exceptions=(PayloadError,))
    if data:
        res = {'name': None, 'uuid': None,'skins': [], 'capes': []}
        res['uuid'] = data['id']
        res['name'] = data['name']

        for d in data['properties']:
            textures = json.loads(urlsafe_b64decode(d['value']))['textures']
            if 'SKIN' in textures.keys():
                res['skins'].append(Skin(textures['SKIN']['url'], textures['SKIN'].get('metadata',{}).get('model','classic')))
            if 'CAPE' in textures.keys():
                res['skins'].append(Cape(textures['CAPE']['url']))

        return res
