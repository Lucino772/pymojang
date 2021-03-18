from .urls import SECURITY_CHECK, SECURITY_CHALLENGES
from ..error.handler import handle_response
from ..error.exceptions import *


def is_secure(session):
    response = session.get(SECURITY_CHECK)
    try:
        handle_response(response, PayloadError, Unauthorized, IPNotSecured)
    except IPNotSecured:
        return False
    else:
        return True

def get_challenges(session):
    response = session.get(SECURITY_CHALLENGES)
    handle_response(response, PayloadError, Unauthorized)
    return data

def verify_ip(session, answers: list):
    response = session.post(SECURITY_CHECK, json=answers)
    try:
        handle_response(response, PayloadError, Unauthorized, IPVerificationError)
    except IPVerificationError:
        return False
    else:
        return True
