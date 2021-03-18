import datetime as dt
import json
from base64 import urlsafe_b64decode

import requests

from ..context import Context
from ..error.exceptions import *
from ..utils.cape import Cape
from ..utils.skin import Skin
from .urls import (CHANGE_NAME, CHECK_NAME_CHANGE, GET_AUTH_PROFILE, GET_PROFILE, RESET_SKIN, UPLOAD_SKIN)
from .validator import default_context, validate_context


@default_context
@validate_context
def check_name_change(ctx: Context) -> dict:
    """
    Retrieve information about name change, only works with context

    Required context variables
    --------------------------
    session: requests.Session

    Returns
    -------
    A dict with the following values: `created_at` and `name_change_allowed`
    """
    res = dict.fromkeys(('created_at','name_change_allowed'), None)

    if 'Authorization' in ctx.session.headers.keys():
        data = ctx.request('get', CHECK_NAME_CHANGE, exceptions=(PayloadError, Unauthorized))
        res.update({
            'created_at': dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
            'name_change_allowed': data['nameChangeAllowed']
        })
    
    return res

@validate_context
def change_name(ctx: Context, name: str):
    """
    Change name, only works with context

    Required context variables
    --------------------------
    session: requests.Session

    Parameters
    ----------
    name: str
    """
    ctx.request('put', CHANGE_NAME.format(name=name), exceptions=(InvalidName, UnavailableName, Unauthorized))

@validate_context
def upload_skin(ctx: Context, path: str, variant='classic'):
    """
    Change skin, only works with context

    Required context variables
    --------------------------
    session: requests.Session

    Parameters
    ----------
    path: str
        Local file or url path
    """
    skin = Skin(path, variant=variant)
    files = [
        ('variant', skin.variant),
        ('file', (f'image.{skin.file.extention}', skin.data, f'image/{skin.file.extention}'))
    ]
    ctx.request('post', UPLOAD_SKIN, exceptions=(PayloadError, Unauthorized), files=files, headers={'content-type': None})

@validate_context
def reset_skin(ctx: Context, uuid: str):
    """
    Reset skin for given `uuid`, only works with context

    Required context variables
    --------------------------
    session: requests.Session

    Parameters
    ----------
    uuid: str
    """
    ctx.request('delete', RESET_SKIN.format(uuid=uuid), exceptions=(PayloadError, Unauthorized))

@default_context
@validate_context
def get_profile(ctx: Context, uuid=None) -> dict:
    """
    Retrieve profile information about player, works with or
    without context.

    If a context is given with a valid `session`, data will
    be loaded using the `session`.

    If the context is not given, the `uuid` will be used to
    retrieve the profile data.

    Returns
    -------
    A dict with the following values: `uuid`, `name`, `skins` and `capes`
    """
    res = dict.fromkeys(('uuid','name','skins','capes'), None)

    if 'Authorization' in ctx.session.headers.keys():
        data = ctx.request('get', GET_AUTH_PROFILE, exceptions=(PayloadError, Unauthorized))
        
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
        data = ctx.request('get', GET_PROFILE.format(uuid=uuid), exceptions=(PayloadError,))

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
