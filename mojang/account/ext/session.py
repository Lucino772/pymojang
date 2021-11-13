from typing import Optional

from ..auth import yggdrasil
from ._profile import MojangAuthenticatedUser


def connect(
    username: str, password: str, client_token: Optional[str] = None
) -> "MojangAuthenticatedUser":
    """Connect a user with name and password

    Args:
        username (str): The username or email if account is not legacy
        password (str): The user password
        client_token (str, optional): The client token to use in the authentication (default to None)

    Returns:
        MojangAuthenticatedUser

    Example:

        ```python
        import mojang

        session = mojang.connect('USERNAME_OR_EMAIL', 'PASSWORD')
        print(session)
        ```
        ```bash
        MojangAuthenticatedUser(
            name='PLAYER_NAME',
            uuid='PLAYER_UUID',
            is_legacy=False,
            is_demo=False,
            names=(NameInfo(name='PLAYER_NAME', changed_to_at=None),),
            skin=Skin(source='http://...', variant='classic'),
            cape=None,
            created_at=datetime.datetime(2006, 4, 29, 10, 10, 10),
            name_change_allowed=True
        )
        ```
    """
    access_token, client_token = yggdrasil.authenticate(
        username, password, client_token
    )
    return MojangAuthenticatedUser(access_token, client_token)
