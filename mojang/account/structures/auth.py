from typing import NamedTuple


## Authentication 
class AuthenticationInfo(NamedTuple):
    """
    Attributes:
        access_token (str): The session's access token
        client_token (str): The session's client token
        uuid (str): The uuid of the player
        name (str): The name of the player
        legacy (bool): Wether the account has migrated
        demo (bool): Wether the account is demo 
    """
    access_token: str
    client_token: str
    uuid: str
    name: str
    legacy: bool
    demo: bool

## Security
class ChallengeInfo(NamedTuple):
    """
    Attributes:
        id (int): The id of the challenge
        challenge (str): The challenge to complete
    """
    id: int
    challenge: str
