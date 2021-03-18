from ..context import Context
from ..error.exceptions import *
from .urls import SECURITY_CHALLENGES, SECURITY_CHECK
from .validator import validate_context


@validate_context
def is_secure(ctx: Context) -> bool:
    """
    Return if IP is verified, works only with context

    Required context variables
    --------------------------
    session: requests.Session

    Returns
    -------
    True if verified else False
    """
    try:
        ctx.request('get', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPNotSecured))
    except IPNotSecured:
        return False
    else:
        return True

@validate_context
def get_challenges(ctx: Context) -> list:
    """
    Return the challenges to verify ip, works only with context

    Required context variables
    --------------------------
    session: requests.Session

    Returns
    -------
    A list of challenges
    """
    data = ctx.request('get', SECURITY_CHALLENGES, exceptions=(PayloadError, Unauthorized))
    return data

@validate_context
def verify_ip(ctx: Context, answers: list) -> bool:
    """
    Verify IP, works only with context

    Required context variables
    --------------------------
    session: requests.Session

    Parameters
    ----------
    answers: list
        list of answers to each challenges

    Returns
    -------
    True if verified else False
    """
    try:
        ctx.request('post', SECURITY_CHECK, exceptions=(PayloadError, Unauthorized, IPVerificationError), json=answers)
    except IPVerificationError:
        return False
    else:
        return True
