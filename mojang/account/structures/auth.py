from dataclasses import dataclass, field

## Authentication 
@dataclass(frozen=True)
class AuthenticationInfo:
    access_token: str = field()
    client_token: str = field()
    uuid: str = field()
    name: str = field()
    legacy: bool = field(default=False)
    demo: bool = field(default=False)

## Security
@dataclass(frozen=True)
class ChallengeInfo:
    id: int = field()
    challenge: str = field()
