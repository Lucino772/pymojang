import requests
import datetime as dt
import json
from base64 import urlsafe_b64decode
from ..urls import MINECRAFT_SERVICES, MOJANG_SESSION
from .skin import Skin
from .cape import Cape
from . import api

class UserProperty:

    def __init__(self, name: str, fct):
        self.__name = name
        self.__fct = fct

    def __get__(self, obj, cls):
        property_name =  f'_{cls.__name__}__{self.__name}'
        if hasattr(obj, property_name):
            return getattr(obj, property_name)
        else:
            getattr(obj, self.__fct.__name__)()
            return getattr(obj, property_name)

class UserProfile:

    def __init__(self, session: requests.Session, username=None, authenticated=False, load=False):
        self.__session = session
        self.__username = username
        self.__authenticated = authenticated

        if self.__authenticated:
            self._load_profile()
            self.__username = self.__name
            self._load_uuid()
        else:
            self._load_uuid()

        if load:
            self._load_names()
            self._load_name_change()
            if not self.__authenticated:
                self._load_profile()
            
    def _load_uuid(self):
        data = api.uuid(self.__username, only_uuid=False)
        self.__user_id = data['id']
        self.__name = data['name']
        self.__legacy = data.get('legacy', False)
        self.__demo = data.get('demo', False)

    def _load_names(self):
        self.__names = api.names(self.__user_id)

    def _load_name_change(self):
        if self.__authenticated:
            url = MINECRAFT_SERVICES.join('minecraft/profile/namechange')
            response = self.__session.get(url)
            if response.status_code == 200:
                data = response.json()
                self.__created_at = dt.datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
                self.__name_change_allowed = data['nameChangeAllowed']
            else:
                pass
        else:
            self.__created_at = None
            self.__name_change_allowed = None
    
    def _load_profile(self):
        if self.__authenticated:
            url = MINECRAFT_SERVICES.join('minecraft/profile')
            response = self.__session.get(url)

            if response.status_code == 200:
                data = response.json()
                self.__user_id = data['id']
                self.__name = data['name']

                self.__skins = []
                self.__capes = []

                for skin in data['skins']:
                    self.__skins.append(Skin(skin['url'], skin['variant'].lower()))
                
                for cape in data['capes']:
                    self.__capes.append(Cape(cape['url']))
        else:
            url = MOJANG_SESSION.join('session/minecraft/profile/{}'.format(self.__user_id))
            response = self.__session.get(url)

            if response.status_code == 200:
                data = response.json()
                self.__skins = []
                self.__capes = []
                
                for d in data['properties']:
                    textures = json.loads(urlsafe_b64decode(d['value']))['textures']
                    if 'SKIN' in textures.keys():
                        self.__skins.append(Skin(textures['SKIN']['url'], textures['SKIN'].get('metadata',{}).get('model','classic')))
                    if 'CAPE' in textures.keys():
                        self.__capes.append(Cape(textures['CAPE']['url']))

    name = UserProperty('name', _load_uuid)
    uuid = UserProperty('user_id', _load_uuid)
    is_legacy = UserProperty('legacy', _load_uuid)
    is_demo = UserProperty('demo', _load_uuid)

    names = UserProperty('names', _load_names)

    created_at = UserProperty('created_at', _load_name_change)
    name_change_allowed = UserProperty('name_change_allowed', _load_name_change)

    skins = UserProperty('skins', _load_profile)
    capes = UserProperty('capes', _load_profile)

def profile(username: str, load=False):
    return UserProfile(requests.Session(), username=username, load=load)
