import requests

from ._urls import URLs
from ._structures import *

# TODO: Handle errors and exception

def status():
    response = requests.get(URLs.status_check())

    _status = []
    for service in response.json():
        item = list(service.items())[0]
        _status.append(ServiceStatus(name=item[0], status=item[1]))
    
    return StatusCheck(_status)

def get_uuid(username: str):
    response = requests.get(URLs.uuid(username))

    data = response.json()
    data['uuid'] = data.pop('id')

    return UUIDInfo(**data)

def get_uuids(usernames: list):
    usernames = list(map(lambda u: u.lower(), usernames))
    _uuids = [None]*len(usernames)

    for i in range(0, len(usernames), 10):
        response = requests.post(URLs.uuids(), json=usernames[i:i+10])

        for item in response.json():
            index = usernames.index(item['name'].lower())
            item['uuid'] = item.pop('id')
            _uuids[index] = UUIDInfo(**item)

    return _uuids

def names(uuid: str):
    response = requests.get(URLs.name_history(uuid))

    _names = []
    for item in response.json():
        changed_to_at = None
        if 'changedToAt' in item.keys():
            changed_to_at = dt.datetime.fromtimestamp(item['changedToAt'] / 1000)
        _names.append(NameInfo(name=item['name'], changed_to_at=changed_to_at))

    return NameInfoList(_names)
