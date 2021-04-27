from requests.auth import AuthBase

class BearerAuth(AuthBase):

    def __init__(self, token: str):
        self.__token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.__token)
        return r
