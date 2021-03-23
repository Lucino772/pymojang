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
    """

    __slots__ = ('name', 'uuid', 'is_legacy', 'is_demo', 'names', 'created_at', 'name_change_allowed', 'skins', 'capes')

    @classmethod
    def create(cls, **kwargs):
        profile = UserProfile()
        
        for key, value in kwargs.items():
            if key in cls.__slots__:
                super(cls, profile).__setattr__(key, value) 

        return profile

    def __init__(self):
        self.name: str = None
        self.uuid: str = None
        self.is_legacy: bool = False
        self.is_demo: bool = False

        self.names: list = None

        self.created_at: dt.datetime = None
        self.name_change_allowed: bool = None

        self.skins: list = []
        self.capes: list = []
