[![PyPI](https://img.shields.io/pypi/v/pymojang)](https://pypi.org/project/pymojang/)
[![Read the Docs](https://img.shields.io/readthedocs/pymojang)](https://pymojang.readthedocs.io/en/latest/)
[![CI](https://github.com/Lucino772/pymojang/actions/workflows/ci.yml/badge.svg)](https://github.com/Lucino772/pymojang/actions/workflows/ci.yml)
[![pre-commit](https://github.com/Lucino772/pymojang/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/Lucino772/pymojang/actions/workflows/pre-commit.yml)
[![codecov](https://codecov.io/gh/Lucino772/pymojang/branch/main/graph/badge.svg?token=5Q6PRUXL4T)](https://codecov.io/gh/Lucino772/pymojang)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymojang)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymojang)

# Pymojang
PyMojang is a full wrapper of the [Mojang API](https://wiki.vg/Mojang_API) and [Mojang Authentication API](https://wiki.vg/Authentication).
It also support the [Microsoft Authentication Scheme](https://wiki.vg/Microsoft_Authentication_Scheme).

## Installation

To install the library use the following command:

```bash
pip install pymojang
```

## Usage

Retrieve information about a user

```python
import mojang
profile = mojang.user('Notch')
print(profile.uuid)
# '069a79f444e94726a5befca90e38aaf5'
print(profile.skin.source)
# 'http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680'
```

Checkout the [documentation](https://pymojang.readthedocs.io/en/latest/)

## V2 Roadmap

`mojang.account` is going to be renamed to `mojang.api`.

### Mojang API (mojang.api.base)

New features:
- [x] `get_sales`: This function retrieve sales statistics. :exclamation: This method has been removed, the endpoint for statistics is no longer active
- [x] `get_blocked_servers` : This function retrieve blocked server hashes
- [x] `get_username` : This function return the username for a given uuid

The following functions are going to be renamed:
- [x] `status` &rarr; `get_status`
- [x] `names` &rarr; `get_names`
- [x] `user` &rarr; `get_profile`

Improvements:
- [x] `get_uuid` returns the uuid
- [x] `get_uuids` returns a dict<str, str>
- [x] `get_status` returns a list of ServiceStatus
- [x] `get_names` returns a sorted list of NameInfo

### Authentication (mojang.api.auth.*)

The following features will be removed:
- [x] `connect`
- [x] `microsoft_app`

And replaced by:
- [x] `app`

### Session API (mojang.api.session)

New features:
- [x] `check_product_voucher` : Check if a product voucher is valid
- [x] `redeem_product_voucher` : Redeem a gift code
- [x] `check_username` : Check if a username is available

### Realms API (mojang.api.realms)

Later in V2 the **Realms API** will also be added

### Minecraft

#### Game Files (mojang.minecraft.files.*)

New features:
- [ ] `get_versions` : Get a list of all the minecraft versions
- [ ] `get_version`: Get a specific version

#### Game Protocol (mojang.minecraft.proto.*)

The following features will be moved/renamed:
- [ ] `rcon.session` &rarr; `rcon`
- [ ] `query.get_stats` &rarr; `get_stats`
- [ ] `slp.ping` &rarr; `ping`

Going forward, the **Minecraft Protocol** will be implemented

## Licence
This project uses a
**MIT** Licence [view](https://github.com/Lucino772/pymojang/blob/main/LICENSE)
