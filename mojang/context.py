import requests

from .error.handler import handle_response
from .globals import current_ctx


class Context:
    METHODS = ['request']

    def __enter__(self):
        for method in self.METHODS:
            setattr(current_ctx, method, getattr(self, method))

        current_ctx.__dict__.update(self.__dict__)

    def __exit__(self, *args):
        for method in self.METHODS:
            delattr(current_ctx, method)

        self.__dict__.update(current_ctx.__dict__)
        for key in set(current_ctx.__dict__.keys()):
            delattr(current_ctx, key)
    
    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)
        return self
    
    def request(self, method: str, url: str, exceptions=[], **kwargs):
        if not hasattr(self, 'session'):
            raise NotImplementedError('This function can\'t work because the session object is missing')
        
        method_fct = getattr(self.session, method)
        response = method_fct(url, **kwargs)
        data = handle_response(response, *exceptions)
        return data
