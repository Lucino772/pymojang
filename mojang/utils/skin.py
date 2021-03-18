import re
from os import path

from .web import WebFile

class Skin:

    def __init__(self, filename: str, variant='classic'):
        self.__filename = filename
        self.__variant = variant
        self.__file = WebFile(self.__filename)

    @property
    def variant(self):
        return self.__variant

    @property
    def file(self):
        return self.__file

    @property
    def data(self):
        return self.__file.data()

    def save(self, dest: str):
        return self.__file.save(dest)
