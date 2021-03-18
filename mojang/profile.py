import datetime as dt


class UserProfile:
    """
    This class represent a Mojang user profile

    Attributes
    ----------
    name:  str
        the player name
    uuid: str
        the player uuid
    is_legacy: bool
        True if user has not migrated to mojang account
    is_demo: bool
        True if user has not paid
    names: list
        the player name history
    created_at: dt.datetime
        The player date of creation
    name_change_allowed: bool
        True if player can change name
    skins: list
        the list of skins
    capes: list
        the list of capes

    Methods
    -------
    update(**kwargs)
        Update given profile properties
    """

    def __init__(self, name: str, uuid: str, legacy: bool, demo: bool, names: list, created_at: dt.datetime, name_change_allowed: bool, skins: list, capes: list):
        self.name = name
        self.uuid = uuid
        self.is_legacy = legacy
        self.is_demo = demo

        self.names = names

        self.created_at = created_at
        self.name_change_allowed = name_change_allowed

        self.skins = skins
        self.capes = capes

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
