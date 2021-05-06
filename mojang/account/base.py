import base64
import json
from dataclasses import fields

import requests

from ..exceptions import handle_response
from ._structures import *
from ._urls import URLs


def status():
    response = requests.get(URLs.status_check())
    data = handle_response(response)

    _status = []
    for service in data:
        item = list(service.items())[0]
        _status.append(ServiceStatus(name=item[0], status=item[1]))
    
    return StatusCheck(_status)

def get_uuid(username: str):
    response = requests.get(URLs.uuid(username))
    data = handle_response(response)

    data['uuid'] = data.pop('id')

    return UUIDInfo(**data)

def get_uuids(usernames: list):
    usernames = list(map(lambda u: u.lower(), usernames))
    _uuids = [None]*len(usernames)

    for i in range(0, len(usernames), 10):
        response = requests.post(URLs.uuids(), json=usernames[i:i+10])
        data = handle_response(response)

        for item in data:
            index = usernames.index(item['name'].lower())
            item['uuid'] = item.pop('id')
            _uuids[index] = UUIDInfo(**item)

    return _uuids

def names(uuid: str):
    response = requests.get(URLs.name_history(uuid))
    data = handle_response(response)

    _names = []
    for item in data:
        changed_to_at = None
        if 'changedToAt' in item.keys():
            changed_to_at = dt.datetime.fromtimestamp(item['changedToAt'] / 1000)
        _names.append(NameInfo(name=item['name'], changed_to_at=changed_to_at))

    return NameInfoList(_names)

def user(uuid: str):
    response = requests.get(URLs.profile(uuid))
    data = handle_response(response)
    _dict = dict.fromkeys([f.name for f in fields(UserProfile) if f.init], None)

    # Load profile info
    _dict['name'] = data['name']
    _dict['uuid'] = uuid
    _dict['is_legacy'] = data.get('legacy', False)
    _dict['is_demo'] = data.get('demo', False)

    # Load skin and cape
    textures_data = json.loads(base64.b64decode(data['properties'][0]['value']))
    
    skin_data = textures_data['textures'].get('SKIN', None)
    if skin_data:
        _dict['skin'] = Skin(skin_data['url'], skin_data.get('metadata', {'model': 'classic'})['model']) 

    cape_data = textures_data['textures'].get('CAPE', None)
    if cape_data:
        _dict['cape'] = Cape(cape_data['url'])

    # Get name history
    _dict['names'] = names(uuid)

    return UserProfile(**_dict)
