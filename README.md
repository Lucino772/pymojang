[![Read the Docs](https://img.shields.io/readthedocs/pymojang?style=flat-square)](https://pymojang.readthedocs.io/en/latest/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pymojang?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymojang?style=flat-square)

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

## Licence
This project uses a
**MIT** Licence [view](https://github.com/Lucino772/pymojang/blob/main/LICENSE)