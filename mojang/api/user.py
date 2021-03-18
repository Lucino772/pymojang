import datetime as dt
import json
from base64 import urlsafe_b64decode

import requests

from ..error.exceptions import *
from ..error.handler import handle_response
from ..utils.cape import Cape
from ..utils.skin import Skin
from .urls import (CHANGE_NAME, CHECK_NAME_CHANGE, GET_AUTH_PROFILE, GET_PROFILE, RESET_SKIN, UPLOAD_SKIN)


def check_name_change(session: requests.Session):
    res = dict.fromkeys(('created_at','name_change_allowed'), None)

    if 'Authorization' in session.headers.keys():
        response = session.get(CHECK_NAME_CHANGE)
        data = handle_response(response, PayloadError, Unauthorized)
        res.update({
            'created_at': dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
            'name_change_allowed': data['nameChangeAllowed']
        })
    
    return res

def change_name(session: requests.Session, name: str):
    response = session.put(CHANGE_NAME)
    handle_response(response, InvalidName, UnavailableName, Unauthorized)

def upload_skin(session: requests.Session, path: str, variant='classic'):
    skin = Skin(path, variant=variant)
    skin_data = skin.data
    files = [
        ('variant', variant),
        ('file', (f'image.{skin.extension[1:]}', skin_data, f'image/{skin.extension[1:]}'))
    ]

    response = session.post(UPLOAD_SKIN, files=files, headers={'Content-Type': None})
    handle_response(response, PayloadError, Unauthorized)

def reset_skin(session: requests.Session):
    response = session.delete(RESET_SKIN)
    handle_response(response, PayloadError, Unauthorized)

def get_profile(session: requests.Session, uuid=None):
    res = dict.fromkeys(('uuid','name','skins','capes'), None)

    if 'Authorization' in session.headers.keys():
        response = session.get(GET_AUTH_PROFILE)
        data = handle_response(response, PayloadError, Unauthorized)
        
        res.update({
            'uuid': data['id'],
            'name': data['name'],
            'skins': [],
            'capes': []
        })

        for skin in data['skins']:
            res['skins'].append(Skin(skin['url'], skin['variant'].lower()))
        
        for cape in data['capes']:
            res['skins'].append(Cape(cape['url']))
    else:
        response = session.get(GET_PROFILE.format(uuid=uuid))
        data = handle_response(response, PayloadError)

        res.update({
            'uuid': data['id'],
            'name': data['name'],
            'skins': [],
            'capes': []
        })
        
        for d in data['properties']:
            textures = json.loads(urlsafe_b64decode(d['value']))['textures']
            if 'SKIN' in textures.keys():
                res['skins'].append(Skin(textures['SKIN']['url'], textures['SKIN'].get('metadata',{}).get('model','classic')))
            if 'CAPE' in textures.keys():
                res['skins'].append(Cape(textures['CAPE']['url']))
        
    return res
