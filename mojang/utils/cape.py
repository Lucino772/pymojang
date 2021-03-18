import re
from os import path

from .web import WebFile

class Cape:

    def __init__(self, filename: str):
        self.__filename = filename
        self.__file = WebFile(self.__filename)

    @property
    def file(self):
        return self.__file

    @property
    def data(self):
        return self.__file.data()

    def save(self, dest: str):
        return self.__file.save(dest)
