import re
from os import path
from urllib.parse import urljoin, urlparse

import requests
import validators
from requests.auth import AuthBase

from ..error.handler import handle_response


class URL:

    def __init__(self, root: str):
        self.__root = root

    def join(self, *paths):
        base = self.__root
        for path in paths:
            base = urljoin(base, path)
        return base
    
    @property
    def root(self):
        return self.__root


# Download
class Downloadable:

    def __init__(self, source: str):
        self.__source = source
        self.__filename = []
        self.__data = None

        if validators.url(self.__source):
            response = download_bytes(self.__source)
            if response:
                self.__filename, self.__data = response
            else:
                raise Exception('Invalid source')
        elif path.exists(self.__source):
            basename = path.basename(self.__source)
            self.__filename = path.splitext(basename)
            self.__filename[1] = self.__filename[1][1:]
            with open(self.__source, 'rb') as fp:
                self.__data = fp.read()
        else:
            raise Exception('Invalid source')

    @property
    def source(self):
        return self.__source

    @property
    def filename(self):
        return '.'.join(self.__filename)

    @property
    def name(self):
        return self.__filename[0]

    @property
    def extension(self):
        return self.__filename[1]

    @property
    def data(self):
        return self.__data

    @property
    def size(self):
        return len(self.__data)

    def save(self, dest: str):
        file_path = dest
        if path.isdir(dest):
            file_path = path.join(dest, self.filename)
        elif not dest.endswith(self.extension):
            file_path = dest + f'.{self.extension}'
        
        with open(file_path, 'wb') as fp:
            fp.write(self.data)

# Auth
class BearerAuth(AuthBase):

    def __init__(self, token: str):
        self.__token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.__token)
        return r

# Download
def filename_from_url(url: str):
    url_path = urlparse(url).path
    match = re.match('^([\w,\s-]+)\.([A-Za-z]{3})$', path.basename(url_path))
    if match:
        return match.groups()

def filename_from_headers(headers: dict):
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

def download_bytes(url: str):
    response = requests.get(url)
    if response.ok:
        filename = filename_from_headers(response.headers) or filename_from_url(url) or ['download', None]
        return filename, response.content

# Request
def request(method: str, url: str, exceptions=[], **kwargs):
    method_fct = getattr(requests, method)
    response = method_fct(url, **kwargs)
    data = handle_response(response, *exceptions)
    return data

def auth_request(method: str, url: str, token: str, exceptions=[], **kwargs):
    return request(method, url, exceptions=exceptions, auth=BearerAuth(token), **kwargs)
