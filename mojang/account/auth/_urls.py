
class URLs:

    # Auth
    @classmethod
    def authenticate(cls):
        return 'https://authserver.mojang.com/authenticate'

    @classmethod
    def refresh(cls):
        return 'https://authserver.mojang.com/refresh'

    @classmethod
    def validate(cls):
        return 'https://authserver.mojang.com/validate'

    @classmethod
    def invalidate(cls):
        return 'https://authserver.mojang.com/invalidate'

    @classmethod
    def signout(cls):
        return 'https://authserver.mojang.com/signout'
