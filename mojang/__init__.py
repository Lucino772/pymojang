"""
Pymojang module
---------------

Pymojang is a full wrapper around the [Mojang API](https://wiki.vg/Mojang_API)
and [Mojang Authentication API](https://wiki.vg/Authentication)

Checkout the [`documentation`](https://pymojang.readthedocs.io/en/latest/)
"""
from .api import (
    get_uuid,
    get_uuids,
    get_names,
    get_status,
    get_sales,
    get_profile,
    connect,
    microsoft_app,
)

from . import _version

__version__ = _version.get_versions()["version"]
