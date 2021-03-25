from .api import base, session
from .api.auth import security, yggdrasil
from .profile import UserProfile


class UserSession(UserProfile):
    """This class represent a Mojang authenticated user

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

    def __init__(self, access_token: str, client_token: str):
        super().__init__()
        self.__access_token = access_token
        self.__client_token = client_token

        self._refresh()

    def _refresh(self):
        data = yggdrasil.refresh_token(self.__access_token, self.__client_token)
        self.__access_token = data['access_token']
        self.__client_token = data['client_token']

        self.uuid = data['uuid']
        self.name = data['name']
        self.is_legacy = data['legacy']
        self.is_demo = data['demo']

        self._fetch_data()

    def _fetch_data(self):
        # Get name history
        self.names = base.name_history(self.uuid)
        
        # Check name change
        data = session.get_user_name_change(self.__access_token)
        self.name_change_allowed = data['name_change_allowed']
        self.created_at = data['created_at']

        # Fetch skins/capes
        data = base.get_profile(self.uuid)
        # self.uuid = data['uuid']
        self.name = data['name']
        self.skins = data['skins']
        self.capes = data['capes']

    def close(self):
        """Close current session"""
        yggdrasil.invalidate_token(self.__access_token, self.__client_token)
        self.__access_token = None
        self.__client_token = None

    # Security
    @property
    def secure(self) -> bool:
        """Return if user IP is verified"""
        return security.is_user_ip_secure(self.__access_token)

    @property
    def challenges(self) -> list:
        """Return the list of challenges to verify user IP"""
        return security.get_user_challenges(self.__access_token)

    def verify(self, answers: list) -> bool:
        """Verify user IP
        
        Args:
            answers (list): The answers to verify the IP
        """ 
        return security.verify_user_ip(self.__access_token, answers)
    
    # Name
    def change_name(self, name: str):
        """Change user name, and update profile data
        
        Args:
            name (str): The new user name
        """
        session.change_user_name(self.__access_token, name)
        self._fetch_data()

    # Skin
    def change_skin(self, path: str, variant='classic'):
        """Change user skin, and update profile data
        
        Args:
            path (str): The path to the skin
            variant (str, optional): The skin variant, either `classic` or `slim` 
        """
        session.change_user_skin(self.__access_token, path, variant)
        self._fetch_data()

    def reset_skin(self):
        """Reset user skin, and update profile data"""
        session.reset_user_skin(self.__access_token, self.uuid)
        self._fetch_data()

