"""
Authentication
--------------
/authenticate
    - 200 OK
    - 403 Invalid credentials. Invalid username or password.
    - 403 TooManyRequestsException

/refresh
    - 200 OK
    - 403 Invalid Signature
    - 403 Token does not exist: wrong client/access token

/validate
    - 204 OK
    - 403 Invalid Token

/signout
    - 204 OK
    - 403 Invalid credentials. Invalid username or password.
    - 429 TooManyRequestsException

/invalidate
    - 204 OK
    - 403 Invalid Token
    - 400 Bad Request

Mojang API
----------
# Change Name
https://api.minecraftservices.com/minecraft/profile/name/<name>
    - 200 OK
    - 400 Name is invalid, longer than 16 characters or contains characters other than (a-zA-Z0-9_) 
    - 403 Name is unavailable
    - 401 Unauthorized
    - 500 Timed out

# Skin
https://api.minecraftservices.com/minecraft/profile/skins
    - 204 OK
    - 401 Unauthorized

https://api.mojang.com/user/profile/<uuid>/skin
    - 204 OK
    - 401 Unauthorized

# Security
https://api.mojang.com/user/security/location
    - 204 OK
    - 403 Unverified IP
    - 401 Unauthorized

https://api.mojang.com/user/security/challenges
    - 200 OK
    - 401 Unauthorized

https://api.mojang.com/user/security/location (POST)
    - 204 OK
    - 403 Verification Error
    - 401 Unauthorized


# Others
https://api.minecraftservices.com/minecraft/profile
    - 200 OK
    - 401 Unauthorized

https://api.mojang.com/users/profiles/minecraft/<username>
    - 200 OK
    - 204 Player do no exists
    - 400 Malformed username

https://api.mojang.com/user/profiles/<uuid>/names
    - 200 OK
    - 204 Player do not exists
    - 400 Malformed uuid
    - 500 Internal Server Error

https://api.mojang.com/profiles/minecraft
    - 200 OK (peut ne rien avoir trouver)
    - 400 Probleme dans payload

https://sessionserver.mojang.com/session/minecraft/profile/<uuid>
    - 200 OK
    - 204 Player do not exists
    - 400 Malformed uuid

"""



# Errors
E_METHOD_NOT_ALLOWED = 'Method Not Allowed'
E_NOT_FOUND = 'Not Found'
E_UNAUTHORIZED = 'Unauthorized'
E_FORBIDDEN_OPERATION_EXCEPTION = 'ForbiddenOperationException'
E_ILLEGAL_ARGUMENT_EXCEPTION = 'IllegalArgumentException'
E_UNSUPPORTED_MEDIA_TYPE = 'Unsupported Media Type'
E_BAD_REQUEST_EXCEPTION = 'BadRequestException'

# Causes
C_USER_MIGRATED_EXCEPTION = 'UserMigratedException'