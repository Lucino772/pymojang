import base64
import json
from dataclasses import dataclass, field
from typing import List

import requests
from uuid import UUID

from ..account import get_uuid, names
from ..account._structures import Cape, NameInfoList, Skin

def user(uuid_name: str):
    return UserProfile.create(uuid_name)

@dataclass
class UserProfile:
    name: str = field()
    uuid: str = field()
    is_legacy: bool = field()
    is_demo: bool = field()
    names: NameInfoList = field()
    skin: Skin = field()
    cape: Cape = field()

    @staticmethod
    def create(uuid: str):
        try:
            UUID(uuid)
        except:
            uuid = get_uuid(uuid).uuid

        # Fetch profile
        response = requests.get('https://sessionserver.mojang.com/session/minecraft/profile/{}'.format(uuid))
        user_data = response.json()
        data = json.loads(base64.b64decode(user_data['properties'][0]['value']))

        skin_data = data['textures']['SKIN']
        skin = Skin(skin_data['url'], skin_data.get('metadata', {}).get('model', 'classic'))
        cape = Cape(data['textures']['CAPE']['url']) if 'CAPE' in data['textures'] else None

        # Get name history
        name_history = names(uuid)

        return UserProfile(
            name=user_data['name'], 
            uuid=uuid, 
            is_legacy=user_data.get('legacy', False), 
            is_demo=user_data.get('demo', False), 
            names=name_history,
            skin=skin,
            cape=cape
        )
