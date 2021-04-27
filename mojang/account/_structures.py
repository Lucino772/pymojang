import validators
import re
import requests
from os import path
import datetime as dt
from typing import NamedTuple, Tuple, Union

# Status check
class ServiceStatus(NamedTuple):
    name: str
    status: str

class StatusCheck(Tuple[ServiceStatus]):
    
    def get(self, name: str) -> Union[None, ServiceStatus]:
        service = list(filter(lambda s: s.name == name, self))
        if len(service) > 0:
            return service[0]

# UUID and Name
class UUIDInfo(NamedTuple):
    name: str
    uuid: str
    legacy: bool = False
    demo: bool = False

class NameInfo(NamedTuple):
    name: str
    changed_to_at: dt.datetime

class NameInfoList(Tuple[NameInfo]):
    
    @property
    def current(self) -> NameInfo:
        if len(self) == 1:
            return self[0]

        _list = filter(lambda n: n.change_to_at != None, self)
        return max(_list, key=lambda n: n.change_to_at)
    
    @property
    def first(self) -> Union[None, NameInfo]:
        first = list(filter(lambda n: n.changed_to_at == None, self))
        if len(first) > 0:
            return first[0]

## Session
class NameChange(NamedTuple):
    allowed: bool
    created_at: dt.datetime

class _SkinCapeBase(NamedTuple):
    source: str
    variant: str = None

    @classmethod
    def _filename_from_url(cls, url: str):
        url_path = urlparse(url).path
        match = re.match('^([\w,\s-]+)\.([A-Za-z]{3})$', path.basename(url_path))
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
    pass

class Cape(_SkinCapeBase):
    pass

## Authentication 
class AuthenticationInfo(NamedTuple):
    access_token: str
    client_token: str
    uuid: str
    name: str
    legacy: bool = False
    demo: bool = False

## Security
class ChallengeInfo(NamedTuple):
    id: int
    challenge: str
