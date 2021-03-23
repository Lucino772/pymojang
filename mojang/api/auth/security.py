from ...error.exceptions import *
from ...utils import web
from ..urls import SECURITY_CHALLENGES, SECURITY_CHECK


def is_user_ip_secure(access_token: str) -> bool:
    try:
        headers = web.get_auth_header(access_token)
        web.request('get', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPNotSecured), headers=headers)
    except IPNotSecured:
        return False
    else:
        return True

def get_user_challenges(access_token: str) -> list:
    headers = web.get_auth_header(access_token)
    data = web.request('get', SECURITY_CHALLENGES, exceptions=(PayloadError, Unauthorized), headers=headers)
    return data

def verify_user_ip(access_token: str, answers: list) -> bool:
    try:
        headers = web.get_auth_header(access_token)
        web.request('post', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPVerificationError), json=answers, headers=headers)
    except IPVerificationError:
        return False
    else:
        return True
