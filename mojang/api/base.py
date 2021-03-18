import requests

from ..error.exceptions import PayloadError
from ..error.handler import handle_response
from ..globals import current_ctx
from .urls import GET_UUID, GET_UUIDS, NAME_HISTORY, STATUS_CHECK
from .validator import default_context


@default_context
def status(service=None):
    res = {}
    data = current_ctx.request('get', STATUS_CHECK)
    for status in data:
        res.update(status)

    if service:
        return res[service]
    
    return res

@default_context
def names(player_id: str):
    names = []
    data = current_ctx.request('get', NAME_HISTORY.format(uuid=player_id))
    for item in data:
        if 'changedToAt' in item:
            item['changedToAt'] = dt.datetime.fromtimestamp(item['changedToAt'])
        names.append((item['name'], item.get('changedToAt',None)))
        
    return names

@default_context
def uuid(username: str, only_uuid=True):
    data = current_ctx.request('get', GET_UUID.format(name=username))
    data['uuid'] = data.pop('id')
    data['legacy'] = data.get('legacy', False)
    data['demo'] = data.get('demo', False)
    if only_uuid:
        return data['uuid']
    
    return data
    
@default_context
def uuids(usernames: list, only_uuid=True):
    res = []
    if len(usernames) > 0:
        data = current_ctx.request('post', GET_UUIDS, exceptions=(PayloadError,),json=usernames[:10])

        res = list(map(lambda pdata: {
            'uuid': pdata['id'],
            'name': pdata['name'], 
            'legacy': pdata.get('legacy',False),
            'demo': pdata.get('demo', False)
        }, data))
        if only_uuid:
            res = list(map(lambda pdata: pdata['uuid'], res))

        if len(usernames[:10]) > 0:
            res.extend(uuids(usernames[10:], only_uuid=only_uuid))

    return res
