from ..urls import MOJANG_API

def is_secure(session):
    url = MOJANG_API.join('user/security/location')
    response = session._request('get', url)
    return response.status_code == 204

def get_challenges(session):
    url = MOJANG_API.join('user/security/challenges')
    response = session._request('get', url)
    return response.json()

def verify_ip(session, answers: list):
    url = MOJANG_API.join('user/security/location')
    response = session._request('post', url, json=answers)
    return response.status_code == 204
