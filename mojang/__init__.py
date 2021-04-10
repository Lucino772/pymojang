"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API) 
and [Mojang Authentication API](https://wiki.vg/Authentication)

Example - Retrieve basic user information
    
    >>> import mojang
    >>> profile = mojang.user('Notch')
    >>> print(profile.uuid)
    '069a79f444e94726a5befca90e38aaf5'
    >>> print(profile.skins[0].source)
    'http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680'
    >>> ...

Example - Connect with password
    >>> import mojang
    >>> session = mojang.connect('Notch', 'notch_secret_password')
    >>> print(session.uuid)
    '069a79f444e94726a5befca90e38aaf5'
    >>> print(profile.skins[0].source)
    'http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680'
    >>> ...
"""

from .main import (api_status, connect, get_username, get_uuid, get_uuids,
                   name_history, user, mcversions)
