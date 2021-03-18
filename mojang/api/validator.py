from functools import wraps

import requests

from ..context import Context
from ..globals import current_ctx


def validate_context(fct):
    @wraps(fct)
    def _wrapper(*args, **kwargs):
        ctx = kwargs.get('ctx', current_ctx)

        if not hasattr(ctx, 'session') or not isinstance(ctx.session, requests.Session):
            raise RuntimeError(f'{fct.__name__} was called without context')

        return fct(*args, ctx=ctx, **kwargs)
    return _wrapper

def default_context(fct):
    @wraps(fct)
    def _wrapper(*args, **kwargs):
        if hasattr(current_ctx, 'session') and isinstance(current_ctx.session, requests.Session):
            return fct(*args, **kwargs)
        else:
            with Context()(session=requests.Session()):
                return fct(*args, **kwargs)
    return _wrapper
