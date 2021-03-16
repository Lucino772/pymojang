import requests
import json
import datetime as dt
from base64 import urlsafe_b64decode
from .profile import UserProfile
from .skin import Skin
from .cape import Cape
from ..urls import MOJANG_STATUS, MOJANG_API, MOJANG_SESSION

def api_status():
    result = {}
    response = requests.get(MOJANG_STATUS.join('check'))
    if response.status_code == 200:
        data = response.json()

        for status in data:
            for key, value in status.items():
                result[key] = value

    return result

def get_name_history(player_id: str):
    url = MOJANG_API.join('user/profiles/{}/names'.format(player_id))
    response = requests.get(url)

    names = []
    if response.status_code == 200:
        data = response.json()

        for item in data:
            if 'changedToAt' in item:
                item['changedToAt'] = dt.datetime.fromtimestamp(item['changedToAt'])
            names.append((item['name'], item.get('changedToAt',None)))
        
    return names

def get_uuid(username: str, timestamp=None, only_uuid=True):
    url = MOJANG_API.join('users/profiles/minecraft/{}'.format(username))
    params = {'at': timestamp} if timestamp else {}
    
    response = requests.get(url, params=params)
    player_uuid = None
    player_name = None
    player_is_legacy = False
    player_is_demo = False
    if response.status_code == 200:
        data = response.json()

        player_uuid = data['id']
        player_name = data['name']
        player_is_legacy = data.get('legacy', False)
        player_is_demo = data.get('demo', False)

    if only_uuid:
        return player_uuid
    
    return player_uuid, player_name, player_is_legacy, player_is_demo
    
def get_uuids(usernames: list, only_uuid=True):
    url = MOJANG_API.join('profiles/minecraft')
    players_data = []

    if len(usernames) > 0:
        response = requests.post(url, json=usernames)
        
        if response.status_code == 200:
            data = response.json()

            for player_data in data:
                player_uuid = player_data['id']
                player_name = player_data['name']
                player_is_legacy = player_data.get('legacy', False)
                player_is_demo = player_data.get('demo', False)

            if only_uuid:
                players_data.append(player_uuid)
            else:
                players_data.append((player_uuid, player_name, player_is_legacy, player_is_demo))

    return players_data

def get_profile(player_id: str):
    url = MOJANG_SESSION.join('session/minecraft/profile/{}'.format(player_id))
    response = requests.get(url)
    profile = UserProfile()

    profile.names = get_name_history(player_id)

    if response.status_code == 200:
        data = response.json()

        profile.id = data['id']
        profile.name = data['name']
        
        for d in data['properties']:
            textures = json.loads(urlsafe_b64decode(d['value']))['textures']
            if 'SKIN' in textures.keys():
                profile.skins.append(Skin(textures['SKIN']['url'], textures['SKIN'].get('metadata',{}).get('model','classic')))
            if 'CAPE' in textures.keys():
                profile.capes.append(Cape(textures['CAPE']['url']))

    return profile
