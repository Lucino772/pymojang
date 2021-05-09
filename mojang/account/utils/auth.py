from requests.auth import AuthBase


class BearerAuth(AuthBase):

    def __init__(self, token: str):
        self.__token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.__token)
        return r


class URLs:

    # Auth
    @classmethod
    def authenticate(cls):
        """Returns the url to authenticate a user"""
        return 'https://authserver.mojang.com/authenticate'

    @classmethod
    def refresh(cls):
        """Returns the url to refresh an access token"""
        return 'https://authserver.mojang.com/refresh'

    @classmethod
    def validate(cls):
        """Returns the urls to validate an access token"""
        return 'https://authserver.mojang.com/validate'

    @classmethod
    def invalidate(cls):
        """Returns the urls to invalidate an access token"""
        return 'https://authserver.mojang.com/invalidate'

    @classmethod
    def signout(cls):
        """Returns the urls to signout a user"""
        return 'https://authserver.mojang.com/signout'

    ## Security
    @classmethod
    def verify_ip(cls):
        """Returns the url to check and verify user IP"""
        return 'https://api.mojang.com/user/security/location'

    @classmethod
    def get_challenges(cls):
        """Returns the url to get the challenges for user IP verification"""
        return 'https://api.mojang.com/user/security/challenges'

