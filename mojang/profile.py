
class UserProfile:
    """This class represent a Mojang user profile

    Attributes:
        name (str): The player name
        uuid (str): The player uuid
        is_legacy (str): True if user has not migrated to mojang account
        is_demo (str): True if user has not paid
        names (str): The player name history
        created_at (datetime): The player date of creation
        name_change_allowed (str): True if player can change name
        skins (str): The list of skins
        capes (str): The list of capes
    """

    __slots__ = ('name', 'uuid', 'is_legacy', 'is_demo', 'names', 'created_at', 'name_change_allowed', 'skins', 'capes')

    @classmethod
    def create(cls, **kwargs) -> 'UserProfile':
        """Create a new UserProfile from a dict
        
        Args:
            **kwargs (dict): The dict you want to create the profile from
        
        Returns:
            A UserProfile with the attributes from the `kwargs` dict
        """
        profile = UserProfile()
        
        for key, value in kwargs.items():
            if key in cls.__slots__:
                super(cls, profile).__setattr__(key, value) 

        return profile

    def __init__(self):
        self.name = None
        self.uuid = None
        self.is_legacy = False
        self.is_demo = False

        self.names = None

        self.created_at = None
        self.name_change_allowed = None

        self.skins = []
        self.capes = []
