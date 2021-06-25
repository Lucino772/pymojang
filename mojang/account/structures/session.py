import datetime as dt
import re
from os import path
from typing import NamedTuple
from urllib.parse import urlparse

import requests
import validators


class NameChange(NamedTuple):
    """
    Attributes:
        allowed (bool): Wether the user can change name
        created_at (dt.datetime): When was the user created
    """
    allowed: bool
    created_at: dt.datetime

class _SkinCapeBase(NamedTuple):
    source: str
    variant: str = None

    @classmethod
    def _filename_from_url(cls, url: str):
        url_path = urlparse(url).path
        match = re.match(r'^([\w,\s-]+)\.([A-Za-z]{3})$', path.basename(url_path))
        if match:
            return match.groups()

    @classmethod
    def _filename_from_headers(cls, headers: dict):
        # Check content-disposition
        if 'content-disposition' in headers.keys():
            cdisp = headers['content-disposition']
            file_names = re.findall('filename=(.+)', cdisp)
            if len(file_names) > 0:
                return file_names[0][0], file_names[0][1][1:]

        # Check content-type
        if 'content-type' in headers.keys():
            ctype = headers['content-type']
            if (not 'text' in ctype) and (not 'html' in ctype):
                return ctype.split('/')
    
    @classmethod
    def _download_bytes(cls, url: str):
        response = requests.get(url)
        if response.ok:
            filename = cls._filename_from_headers(response.headers) or cls._filename_from_url(url) or ['download', None]
            return filename, response.content

    @property
    def data(self):
        if not hasattr(self, '_data'):
            _data = b''
            _extension = None

            if validators.url(self.source):
                response = self._download_bytes(self.source)
                if response:
                    _extension = response[0][1]
                    _data = response[1]
            elif path.exists(self.source):
                basename = path.basename(self.source)
                _extension = path.splitext(basename)[1][1:]
                
                with open(self.source, 'rb') as fp:
                    _data = fp.read()

            if _extension != 'png':
                pass # TODO: Raise Exception
            
            object.__setattr__(self, '_data', _data)
        
        return self._data

    def save(self, dest: str):
        if not dest.endswith('.png'):
            dest += '.png'
        
        with open(dest, 'wb') as fp:
            fp.write(self.data)

class Skin(_SkinCapeBase):
    """
    Attributes:
        source (str): The source where the skin is located
        variant (str): The variant of skin (default to 'classic')
    """

class Cape(_SkinCapeBase):
    """
    Attributes:
        source (str): The source where the cape is located
    """
