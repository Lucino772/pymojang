
class URLs:
    
    # Base URLs
    @classmethod
    def status_check(cls):
        """Returns the url to check Mojang APIs status"""
        return 'https://status.mojang.com/check'

    @classmethod
    def uuid(cls, username: str):
        """Returns the url to get uuid of username"""
        return f'https://api.mojang.com/users/profiles/minecraft/{username}'

    @classmethod
    def uuids(cls):
        """Returns the url to get uuids of multiple username"""
        return 'https://api.mojang.com/profiles/minecraft'

    @classmethod
    def name_history(cls, uuid: str):
        """Returns the url to get the name history of a user"""
        return f'https://api.mojang.com/user/profiles/{uuid}/names'

    @classmethod
    def profile(cls, uuid: str):
        """Returns the url to get the profile of a user"""
        return f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'

    # Session URLs
    @classmethod
    def name_change(cls):
        """Returns the url to get t name change information"""
        return 'https://api.minecraftservices.com/minecraft/profile/namechange'
    
    @classmethod
    def change_name(cls, name: str):
        """Returns the url to change user's name"""
        return f'https://api.minecraftservices.com/minecraft/profile/name/{name}'
    
    @classmethod
    def change_skin(cls):
        """Returns the url to change the user's skin"""
        return 'https://api.minecraftservices.com/minecraft/profile/skins'
    
    @classmethod
    def reset_skin(cls, uuid: str):
        """Returns the url to reset the user's skin"""
        return f'https://api.mojang.com/user/profile/{uuid}/skin'

    @classmethod
    def check_minecraft_onwership(cls):
        return 'https://api.minecraftservices.com/entitlements/mcstore'

    @classmethod
    def get_profile(cls):
        return 'https://api.minecraftservices.com/minecraft/profile'
