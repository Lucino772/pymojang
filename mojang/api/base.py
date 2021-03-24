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
    res = {}
    
    data = web.request('get', STATUS_CHECK)
    for s in data:
        res.update(s)

    if service:
        return res[service]
    
    return res

def name_history(uuid: str) -> list:
    names = []

    data = web.request('get', NAME_HISTORY.format(uuid=uuid))
    for item in data:
        changed_at = None
        if 'changedToAt' in item.keys():
            changed_at = dt.datetime.fromtimestamp(item['changedToAt'] / 1000)
        names.append((item['name'], changed_at))
    
    return names

def get_uuid(username: str, only_uuid: bool = True) -> dict:
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
