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

### Mojang API

New features:
- [ ] `get_sales`: This function retrieve sales statistics
- [ ] `get_blocked_servers` : This function retrieve blocked server hashes
- [ ] `get_username` : This function return the username for a given uuid

The following functions are going to be renamed:
- [ ] `status` &rarr; `get_status`
- [ ] `names` &rarr; `get_names`
- [ ] `user` &rarr; `get_profile`

### Authentication

The following features will be removed:
- [ ] `connect`
- [ ] `microsoft_app`

And replaced by:
- [ ] `app`

### Session API

New features:
- [ ] `check_giftcode` : Check if redeem code is valid
- [ ] `redeem` : Redeem a gift code
- [ ] `check_name` : Check if a username is available

### Realms API

Later in V2 the **Realms API** will also be added

### Minecraft

#### Game Files

New features:
- [ ] `get_versions` : Get a list of all the minecraft versions
- [ ] `get_version`: Get a specific version

#### Game Protocol

The following features will be moved/renamed:
- [ ] `rcon.session` &rarr; `rcon`
- [ ] `query.get_stats` &rarr; `get_stats`
- [ ] `slp.ping` &rarr; `ping`

Going forward, the **Minecraft Protocol** will be implemented

## Licence
This project uses a
**MIT** Licence [view](https://github.com/Lucino772/pymojang/blob/main/LICENSE)
