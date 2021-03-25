
# Global
class MethodNotAllowed(Exception):
    """The method used for the request is not allowed in the requested url"""
    code = 405

class NotFound(Exception):
    """The requested url doesn't exists"""
    code = 404

class ServerError(Exception):
    """There is an internal error on the requested server"""
    code = 500

class PayloadError(Exception):
    """The data that has been sent to the server is not formated correctly"""
    code = 400

# Authentication Errors
class CredentialsError(Exception):
    """The credentials sent to the server are wrong"""
    code = [403, 429]

class TokenError(Exception):
    """The token sent to the server is invalid"""
    code = 403

class Unauthorized(Exception):
    """The token sent to the server is invalid"""
    code = 401

# Name Change Errors
class InvalidName(Exception):
    """The name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_).
    Only raised when changing the name of a user
    """
    code = 400
    def __init__(self):
        super().__init__("Name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_)")
    
class UnavailableName(Exception):
    """Name is unavailable. Only raised when changing the name of a user"""
    code = 403
    def __init__(self):
        super().__init__("Name is unavailable")

# Security
class IPNotSecured(Exception):
    """The current IP is not secured. Only raised when checking if user IP is secure"""
    code = 403

class IPVerificationError(Exception):
    """Verifiction for IP failed. Only raised when verifying user IP"""
    code = 403
