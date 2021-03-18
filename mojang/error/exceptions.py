
# Global
class MethodNotAllowed(Exception):
    code = 405

class NotFound(Exception):
    code = 404

class ServerError(Exception):
    code = 500

class PayloadError(Exception):
    code = 400

# Authentication Errors
class CredentialsError(Exception):
    code = [403, 429]

class TokenError(Exception):
    code = 403

class Unauthorized(Exception):
    code = 401

# Name Change Errors
class InvalidName(Exception):
    code = 400
    def __init__(self):
        super().__init__("Name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_)")
    
class UnavailableName(Exception):
    code = 403
    def __init__(self):
        super().__init__("Name is unavailable")

# Security
class IPNotSecured(Exception):
    code = 403

class IPVerificationError(Exception):
    code = 403
