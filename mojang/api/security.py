import requests
from .urls import SECURITY_CHECK, SECURITY_CHALLENGES
from ..error.exceptions import *
from .validator import validate_context

@validate_context
def is_secure(ctx):
    try:
        ctx.request('get', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPNotSecured))
    except IPNotSecured:
        return False
    else:
        return True

@validate_context
def get_challenges(ctx):
    data = ctx.request('get', SECURITY_CHALLENGES, exceptions=(PayloadError, Unauthorized))
    return data

@validate_context
def verify_ip(ctx, answers: list):
    try:
        ctx.request('post', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPVerificationError), json=answers)
    except IPVerificationError:
        return False
    else:
        return True
