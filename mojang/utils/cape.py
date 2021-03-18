import requests
import validators
from os import path
import re
from tempfile import SpooledTemporaryFile
from .web import WebFile


class Cape:

    def __init__(self, filename: str):
        self.__filename = filename
        self.__file = None

        if validators.url(self.__filename):
            self.__file = WebFile(self.__filename)
        elif path.exists(filename):
            self.__file = WebFile(path.join('file://', path.abspath(filename)))
        else:
            raise Exception('Invalid filename, must be an `url` or a correct file path')
        
    @property
    def file(self):
        return self.__file

    @property
    def data(self):
        return self.__file.data()

    def save(self, dest: str):
        return self.__file.save(dest)
            
