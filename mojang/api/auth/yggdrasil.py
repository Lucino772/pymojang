"""
Mojang Yggdrasil authentication system api
"""

from ...error.exceptions import *
from ..urls import AUTHENTICATE, INVALIDATE, REFRESH, SIGNOUT, VALIDATE
from ..validator import validate_context


@validate_context
def authenticate(ctx):
    """
    Authenticate with username and password, only works with a context.
    
    Required context variables
    --------------------------
    session: requests.Session
    
    username: str
    
    password: str
    
    client_token: str, optional
        (default is None)

    Returns
    -------
    A dict with the following key: `access_token`, `client_token`, `uuid`, 
    `name`, `legacy` and `demo`
    """
    payload = {
        'username': ctx.username,
        'password': ctx.password,
        'clientToken': getattr(ctx, 'client_token', None),
        'agent': {
            'name': 'Minecraft',
            'version': 1
        }
    }

    data = ctx.request('post', AUTHENTICATE, exceptions=(PayloadError, CredentialsError), json=payload)
    ctx.session.headers.update({'Authorization': 'Bearer {}'.format(data['accessToken'])})

    return {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }

@validate_context
def refresh(ctx):
    """
    Refresh an invalid token, only works with a context.
    
    Required context variables
    --------------------------
    session: requests.Session
    
    access_token: str
    
    client_token: str

    Returns
    -------
    A dict with the following key: `access_token`, `client_token`, `uuid`, 
    `name`, `legacy` and `demo`
    """
    payload = {
        'accessToken': ctx.access_token,
        'clientToken': ctx.client_token
    }

    data = ctx.request('post', REFRESH, exceptions=(PayloadError, TokenError), json=payload)
    ctx.session.headers.update({'Authorization': 'Bearer {}'.format(data['accessToken'])})

    return {
        'access_token': data['accessToken'],
        'client_token': data['clientToken'],
        'uuid': data['selectedProfile']['id'],
        'name': data['selectedProfile']['name'],
        'legacy': data['selectedProfile'].get('legacy', False),
        'demo': not data['selectedProfile'].get('paid', True)
    }

@validate_context
def validate(ctx):
    """
    Check if token is valid, only works with a context.
    
    Required context variables
    --------------------------
    session: requests.Session
    
    access_token: str
    
    client_token: str

    Returns
    -------
    True if valid
    """
    payload = {
        'accessToken': ctx.access_token,
        'clientToken': ctx.client_token
    }

    ctx.request('post', VALIDATE, exceptions=(PayloadError, TokenError), json=payload)
    return True

@validate_context
def signout(ctx):
    """
    Signout with username and password, only works with a context.
    
    Required context variables
    --------------------------
    session: requests.Session
    
    username: str
    
    password: str
    """
    payload = {
        'username': ctx.username,
        'password': ctx.password
    }

    ctx.request('post', SIGNOUT, exceptions=(PayloadError, CredentialsError), json=payload)
    ctx.session.headers.pop('Authorization')

@validate_context
def invalidate(ctx):
    """
    Invalidate current token, only works with a context.
    
    Required context variables
    --------------------------
    session: requests.Session
    
    access_token: str
    
    client_token: str
    """
    payload = {
        'accessToken': ctx.access_token,
        'clientToken': ctx.client_token
    }

    ctx.request('post', INVALIDATE, exceptions=(PayloadError, TokenError), json=payload)
    ctx.session.headers.pop('Authorization')
