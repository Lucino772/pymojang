"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API) 
and [Mojang Authentication API](https://wiki.vg/Authentication)

Checkout the [`documentation`](https://pymojang.readthedocs.io/en/latest/)
"""
from .account import get_uuid, get_uuids, names, status, user, connect, microsoft_app
