# Global
class MethodNotAllowed(Exception):
    """The method used for the request is not allowed"""


class NotFound(Exception):
    """The requested url doesn't exists"""


class ServerError(Exception):
    """There is an internal error on the server"""


class PayloadError(Exception):
    """The data sent to the server has an invalid format"""


# Authentication Errors
class CredentialsError(Exception):
    """The credentials sent to the server are wrong"""


class TokenError(Exception):
    """The token sent to the server has an invalid format"""


class Unauthorized(Exception):
    """The token sent to the server is invalid"""


class MigratedAccount(Exception):
    """Account has been migrated to an Microsoft account,
    you need to use the Microsoft OAuth Flow"""

    def __init__(self, *args):
        super().__init__(
            "Account has been migrated to an Microsoft account, you need to use the Microsoft OAuth Flow"
        )


# Microsoft Authentication Errors
class MicrosoftInvalidGrant(Exception):
    """The auth code or refresh token sent to the server is invalid"""


class XboxLiveAuthenticationError(Exception):
    """Authentication with Xbox Live failed"""


class XboxLiveInvalidUserHash(Exception):
    """The user hash sent to the server is invalid"""


class MicrosoftUserNotOwner(Exception):
    """The Microsoft user does not own Minecraft"""

    def __init__(self, *args):
        super().__init__("The Microsoft user does not own Minecraft")


# Name Change Errors
class InvalidName(Exception):
    """The name is invalid, longer than 16 characters or contains
    characters other than (a-zA-Z0-9_). Only raised when changing
    the name of a user
    """

    def __init__(self, *args):
        super().__init__(
            "Name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_)"
        )


class UnavailableName(Exception):
    """Name is unavailable. Only raised when changing the name of a user"""

    def __init__(self, *args):
        super().__init__("Name is unavailable")


# Cape Errors
class NotCapeOwner(Exception):
    """The user does not own a cape. Only raised when showing a user cape"""

    def __init__(self, *args) -> None:
        super().__init__("User does not own a cape")


# Security
class IPNotSecured(Exception):
    """The current IP is not secured. Only raised when
    checking if user IP is secure
    """


class IPVerificationError(Exception):
    """Verifiction for IP failed. Only raised when verifying user IP"""
