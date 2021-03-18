import requests
from .urls import STATUS_CHECK, NAME_HISTORY, GET_UUID, GET_UUIDS
from ..error.exceptions import PayloadError
from ..error.handler import handle_response


def status(service=None):
    res = {}
    response = requests.get(STATUS_CHECK)
    data = handle_response(response)
    for status in data:
        res.update(status)

    if service:
        return res[service]
    
    return res

def names(player_id: str):
    response = requests.get(NAME_HISTORY.format(uuid=player_id))

    names = []
    data = handle_response(response)
    for item in data:
        if 'changedToAt' in item:
            item['changedToAt'] = dt.datetime.fromtimestamp(item['changedToAt'])
        names.append((item['name'], item.get('changedToAt',None)))
        
    return names

def uuid(username: str, only_uuid=True):
    response = requests.get(GET_UUID.format(name=username))
    data = handle_response(response)
    data['uuid'] = data.pop('id')
    data['legacy'] = data.get('legacy', False)
    data['demo'] = data.get('demo', False)
    if only_uuid:
        return data['uuid']
    
    return data
    
def uuids(usernames: list, only_uuid=True):
    data = {}
    if len(usernames) > 0:
        response = requests.post(GET_UUIDS, json=usernames)
        data = handle_response(response, PayloadError)
        if only_uuid:
            data = list(map(lambda pdata: pdata['id'], data))

    return data
