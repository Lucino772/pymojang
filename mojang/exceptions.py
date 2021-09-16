import json


def handle_response(response, *exceptions, use_defaults=True):
    """Handle response message from http request. Every given `exception`
    must have a `code` property.

    The function will check if the status code from the response is ok.
    If not an Exception will be raised based on the status code.
    """
    if response.ok:
        data = {}
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            pass
        finally:
            return data
    else:
        if use_defaults:
            exceptions += (NotFound, MethodNotAllowed, ServerError)
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            data = {'errorMessage': response.text}
        
        for exception in exceptions:
            if isinstance(exception.code, int):
                if response.status_code == exception.code:
                    raise exception(*data.values())
            elif isinstance(exception.code, list):
                if response.status_code in exception.code:
                    raise exception(*data.values())
        else:
            raise Exception(*data.values())


# Global
class MethodNotAllowed(Exception):
    """The method used for the request is not allowed"""
    code = 405


class NotFound(Exception):
    """The requested url doesn't exists"""
    code = 404


class ServerError(Exception):
    """There is an internal error on the server"""
    code = 500


class PayloadError(Exception):
    """The data sent to the server has an invalid format"""
    code = 400


# Authentication Errors
class CredentialsError(Exception):
    """The credentials sent to the server are wrong"""
    code = [403, 429]


class TokenError(Exception):
    """The token sent to the server has an invalid format"""
    code = 403


class Unauthorized(Exception):
    """The token sent to the server is invalid"""
    code = 401


class MigratedAccount(Exception):
    """Account has been migrated to an Microsoft account,
    you need to use the Microsoft OAuth Flow"""
    code = 410

    def __init__(self, *args):
        super().__init__("Account has been migrated to an Microsoft account, you need to use the Microsoft OAuth Flow")

# Microsoft Authentication Errors
class MicrosoftInvalidGrant(Exception):
    """The auth code or refresh token sent to the server is invalid"""
    code = 400


class XboxLiveAuthenticationError(Exception):
    """Authentication with Xbox Live failed"""
    code = 400


class XboxLiveInvalidUserHash(Exception):
    """The user hash sent to the server is invalid"""
    code = 400


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
    code = 400

    def __init__(self, *args):
        super().__init__("Name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_)")


class UnavailableName(Exception):
    """Name is unavailable. Only raised when changing the name of a user"""
    code = 403

    def __init__(self, *args):
        super().__init__("Name is unavailable")


# Security
class IPNotSecured(Exception):
    """The current IP is not secured. Only raised when
    checking if user IP is secure
    """
    code = 403


class IPVerificationError(Exception):
    """Verifiction for IP failed. Only raised when verifying user IP"""
    code = 403
