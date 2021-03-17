from ..urls import MOJANG_AUTHSERVER

def authenticate(session, username: str, password: str, client_token=None):
    url = MOJANG_AUTHSERVER.join('authenticate')
    payload = {
        'username': username,
        'password': password,
        'clientToken': client_token
    }
    
    response = session._request('post', url, json=payload)
    if response.status_code == 200:
        data = response.json()
        session._update_token(access_token=data['accessToken'], client_token=data['clientToken'])
    else:
        pass

def refresh(session, access_token: str, client_token: str):
    url = MOJANG_AUTHSERVER.join('refresh')
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session._request('post', url, json=payload)
    if response.status_code == 200:
        data = response.json()
        session._update_token(access_token=data['accessToken'], client_token=data['clientToken'])
    else:
        pass

def validate(session, access_token: str, client_token: str):
    url = MOJANG_AUTHSERVER.join('validate')
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session._request('post', url, json=payload)
    return response.status_code == 204

def signout(session, username: str, password: str):
    url = MOJANG_AUTHSERVER.join('signout')
    payload = {
        'username': username,
        'password': password
    }

    response = session._request('post', url, json=payload)
    if response.status_code == 204:
        session._update_token(access_token=None)
        return True
    else:
        return False

def invalidate(session, access_token: str, client_token: str):
    url = MOJANG_AUTHSERVER.join('invalidate')
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = session._request('post', url, json=payload)
    if response.status_code == 204:
        session._update_token(access_token=None)
        return True
    else:
        return False
