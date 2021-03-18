from .exceptions import *

DEFAULTS = [NotFound, MethodNotAllowed, ServerError]

def handle_response(response, *exceptions, use_defaults=True):
    """
    Handle response message from http request. Every given `exception`
    must have a `code` property. 
    
    The function will check if the status code from the response if ok.
    If not an Exception will be raised based on the status code. 
    """
    global DEFAULTS
    if response.ok:
        data = {}
        try:
            data = response.json()
        except ValueError:
            pass
        finally:
            return data
    else:
        if use_defaults:
            exceptions += tuple(DEFAULTS)
        data = response.json()
        for exception in exceptions:
            if isinstance(exception.code, int):
                if response.status_code == exception.code:
                    raise exception(data['errorMessage']) 
            elif isinstance(exception.code, list):
                if response.status_code in exception.code:
                    raise exception(data['errorMessage'])
        else:
            raise Exception(data['error'], data['errorMessage'])
