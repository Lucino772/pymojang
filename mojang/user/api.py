import requests
from ..urls import MOJANG_STATUS, MOJANG_API, MOJANG_SESSION

def status(service=None):
    data = {}
    response = requests.get(MOJANG_STATUS.join('check'))
    if response.status_code == 200:
        for status in response.json():
            data.update(status)

        if service:
            return data[service]
    
    return data

def names(player_id: str):
    url = MOJANG_API.join('user/profiles/{}/names'.format(player_id))
    response = requests.get(url)

    names = []
    if response.status_code == 200:
        data = response.json()

        for item in response.json():
            if 'changedToAt' in item:
                item['changedToAt'] = dt.datetime.fromtimestamp(item['changedToAt'])
            names.append((item['name'], item.get('changedToAt',None)))
        
    return names

def uuid(username: str, timestamp=None, only_uuid=True):
    url = MOJANG_API.join('users/profiles/minecraft/{}'.format(username))
    params = {'at': timestamp} if timestamp else {}
    
    data = {}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if only_uuid:
            return data['id']
    
    return data
    
def uuids(usernames: list, only_uuid=True):
    url = MOJANG_API.join('profiles/minecraft')
    data = []

    if len(usernames) > 0:
        response = requests.post(url, json=usernames)
        
        if response.status_code == 200:
            data = response.json()
            if only_uuid:
                data = list(map(lambda pdata: pdata['id'], data))

    return data
