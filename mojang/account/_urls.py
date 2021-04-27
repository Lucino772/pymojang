
class URLs:
    
    @classmethod
    def status_check(cls):
        return 'https://status.mojang.com/check'

    @classmethod
    def uuid(cls, username: str):
        return f'https://api.mojang.com/users/profiles/minecraft/{username}'

    @classmethod
    def uuids(cls):
        return 'https://api.mojang.com/profiles/minecraft'

    @classmethod
    def name_history(cls, uuid: str):
        return f'https://api.mojang.com/user/profiles/{uuid}/names'
