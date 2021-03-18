"""
Functions for the basic MojangAPI
"""

import datetime as dt

from ..error.exceptions import PayloadError
from ..globals import current_ctx
from .urls import GET_UUID, GET_UUIDS, NAME_HISTORY, STATUS_CHECK
from .validator import default_context


@default_context
def status(service: str = None) -> dict:
    """
    Retrieve the Mojang API status, work without context.

    Parameters
    ----------
    service: str, optional
        If given, return only status for this service (default is None)

    Returns
    -------
    By default it will returns a `dict` where the keys are the 
    services and the values are the status. If service is not 
    None then only the status for the given service is returned. 
    """
    res = {}
    
    data = current_ctx.request('get', STATUS_CHECK)
    for s in data:
        res.update(s)

    if service:
        return res[service]
    
    return res

@default_context
def names(uuid: str) -> list:
    """
    Get the name history for a given uuid, work without context.

    Parameters
    ----------
    uuid: str
    
    Returns
    -------
    A list of tuples. Each tuple contains the `name` and the `datetime`
    it was changed.
    """
    names = []

    data = current_ctx.request('get', NAME_HISTORY.format(uuid=uuid))
    for item in data:
        if 'changedToAt' in item:
            item['changedToAt'] = dt.datetime.fromtimestamp(item['changedToAt'])
        names.append((item['name'], item.get('changedToAt',None)))
    
    return names

@default_context
def uuid(username: str, only_uuid: bool = True) -> dict:
    """
    Return the uuid of a given username

    Parameters
    ----------
    username: str
    only_uuid: bool, optional
        (default is True)
    
    Returns
    -------
    By default it returns only the uuid for the given username. 
    If `only_uuid` is set to false, it will also return the 
    following values `legacy`, `demo` and `name` 
    """
    
    data = current_ctx.request('get', GET_UUID.format(name=username))
    
    data['uuid'] = data.pop('id')
    data['legacy'] = data.get('legacy', False)
    data['demo'] = data.get('demo', False)

    if only_uuid:
        return data['uuid']
    
    return data
    
@default_context
def uuids(usernames: list, only_uuid: bool = True) -> list:
    """
    Return the uuid for multiple username

    Parameters
    ----------
    usernames: list
    only_uuid: bool, optional
        (default is True)
    
    Returns
    -------
    By default it returns only the uuid for each username. 
    If `only_uuid` is set to false, it will also return the 
    following values `legacy`, `demo` and `name` for each
    username.
    """
    res = []

    if len(usernames) > 0:
        data = current_ctx.request('post', GET_UUIDS, exceptions=(PayloadError,),json=usernames[:10])

        for item in data:
            if not only_uuid:
                res.append({
                    'uuid': item['id'],
                    'name': item['name'], 
                    'legacy': item.get('legacy',False),
                    'demo': item.get('demo', False)
                })
            else:
                res.append(item['id'])

        if len(usernames[:10]) > 0:
            res.extend(uuids(usernames[10:], only_uuid=only_uuid))

    return res
