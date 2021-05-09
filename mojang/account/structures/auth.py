from dataclasses import dataclass, field


## Authentication 
@dataclass(frozen=True)
class AuthenticationInfo:
    """
    Attributes:
        access_token (str): The session's access token
        client_token (str): The session's client token
        uuid (str): The uuid of the player
        name (str): The name of the player
        legacy (bool): Wether the account has migrated
        demo (bool): Wether the account is demo 
    """
    access_token: str = field()
    client_token: str = field()
    uuid: str = field()
    name: str = field()
    legacy: bool = field(default=False)
    demo: bool = field(default=False)

## Security
@dataclass(frozen=True)
class ChallengeInfo:
    """
    Attributes:
        id (int): The id of the challenge
        challenge (str): The challenge to complete
    """
    id: int = field()
    challenge: str = field()
