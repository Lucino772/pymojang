import re
from os import path
from urllib.parse import urljoin, urlparse

import requests
import validators


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


class WebFile:

    def __init__(self, url: str, chunk_size=1024):
        self.__url = url
        self.__chunk_size = chunk_size

        self.__filename = None
        self.__extension = None
        self.__data = None

        self._load_info()
        self._load_data()

    def _load_info(self):
        if validators.url(self.__url):
            response = requests.head(self.__url, allow_redirects=True)

            if response.status_code == 200:
                # Find file name and extension
                url_path = urlparse(self.__url).path
                match = re.match('^([\w,\s-]+)\.([A-Za-z]{3})$', path.basename(url_path))
                if match:
                    self.__filename, self.__extension = match.groups()
                elif 'content-disposition' in response.headers.keys():
                    fnames = re.findall('filename=(.+)', response.headers['content-disposition'])
                    if len(fnames) > 0:
                        self.__filename, self.__extension = path.splitext(filename)
                        self.__extension = self.__extension[1:]
                elif 'content-type' in response.headers.keys():
                    content_type = response.headers['content-type']
                    if 'text' not in content_type.lower() and 'html' not in content_type.lower():
                        self.__filename, self.__extension = response.headers['content-type'].split('/')
            else:
                response.raise_for_status()
        else:
            self.__filename, self.__extension = path.splitext(path.basename(self.__url))
            self.__extension = self.__extension[1:]

        if self.__filename is None and self.__extension is None:
            raise Exception('The url/file `{}` can\'t be open'.format(response.url))

    def _load_data(self):
        if validators.url(self.__url):
            response = requests.get(self.__url, allow_redirects=True, stream=True)
            self.__data = response.content
        else:
            with open(self.__url,'rb') as fp:
                self.__data = fp.read()

    @property
    def source(self):
        return self.__url

    @property
    def filename(self):
        return f'{self.__filename}.{self.__extension}'

    @property
    def name(self):
        return self.__filename

    @property
    def extension(self):
        return self.__extension

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
        elif not dest.endswith(self.__extension):
            file_path = dest + f'.{self.__extension}'
        
        with open(file_path, 'wb') as fp:
            fp.write(self.__data)
