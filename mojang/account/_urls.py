
class URLs:
    
    # Base URLs
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

    # Session URLs
    @classmethod
    def name_change(cls):
        return 'https://api.minecraftservices.com/minecraft/profile/namechange'
    
    @classmethod
    def change_name(cls, name: str):
        return f'https://api.minecraftservices.com/minecraft/profile/name/{name}'
    
    @classmethod
    def change_skin(cls):
        return 'https://api.minecraftservices.com/minecraft/profile/skins'
    
    @classmethod
    def reset_skin(cls, uuid: str):
        return f'https://api.mojang.com/user/profile/{uuid}/skin'
