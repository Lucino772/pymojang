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

    # Microsoft
    @classmethod
    def microsoft_xbl_authenticate(cls):
        """Returns the authentication url for Xbox Live"""
        return 'https://user.auth.xboxlive.com/user/authenticate'

    @classmethod
    def microsoft_xbl_authorize(cls):
        """Returns the authorization url for Xbox Live"""
        return 'https://xsts.auth.xboxlive.com/xsts/authorize'

    @classmethod
    def login_with_microsoft(cls):
        """Returns the url to login to minecraft with Xbox Live"""
        return 'https://api.minecraftservices.com/authentication/login_with_xbox'
