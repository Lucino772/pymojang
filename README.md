[![Documentation Status](https://readthedocs.org/projects/pymojang/badge/?version=latest)](https://pymojang.readthedocs.io/en/latest/?badge=latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymojang)

# Pymojang
Pymojang is a full wrapper arround de [Mojang API](https://wiki.vg/Mojang_API) and [Mojang Authentication API](https://wiki.vg/Authentication).

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
print(profile.skins[0].source)
# 'http://textures.minecraft.net/texture/292009a4925b58f02c77dadc3ecef07ea4c7472f64e0fdc32ce5522489362680'
```

Checkout the [documentation](https://pymojang.readthedocs.io/en/latest/)

## Licence
This project uses a
**MIT** Licence [view](https://github.com/Lucino772/pymojang/blob/main/LICENSE)