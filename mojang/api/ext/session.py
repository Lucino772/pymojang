from typing import Optional

from ..auth import yggdrasil
from ._profile import MojangAuthenticatedUser


def connect(
    username: str, password: str, client_token: Optional[str] = None
) -> "MojangAuthenticatedUser":
    """Connect a user with name and password

    :param str username: The username of email if account is not legacy
    :param str password: The user password
    :param client_token: The client token to use
    :type client_token: str or None

    :Example:

    >>> import mojang
    >>> mojang.connect('USERNAME_OR_EMAIL', 'PASSWORD')
    MojangAuthenticatedUser(
        name='PLAYER_NAME',
        uuid='PLAYER_UUID',
        is_legacy=False,
        is_demo=False,
        names=(NameInfo(name='PLAYER_NAME', changed_to_at=None),),
        skins=1,
        capes=0,
        created_at=datetime.datetime(2006, 4, 29, 10, 10, 10),
        name_change_allowed=True
    )
    """
    access_token, client_token = yggdrasil.authenticate(
        username, password, client_token
    )
    return MojangAuthenticatedUser(access_token, client_token)
