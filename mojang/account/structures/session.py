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


class _Resource:
    def __init__(self, source: str, load: bool = True) -> None:
        self.__source = source
        self.__data = bytes()
        self.__extension = None

        if load:
            self.load()

    @property
    def source(self):
        return self.__source

    @property
    def data(self):
        return self.__data

    @property
    def extension(self):
        return self.__extension

    @classmethod
    def _filename_from_url(cls, url: str):
        url_path = urlparse(url).path
        match = re.match(
            r"^([\w,\s-]+)\.([A-Za-z]{3})$", path.basename(url_path)
        )
        if match:
            return match.groups()

    @classmethod
    def _filename_from_headers(cls, headers: dict):
        # Check content-disposition
        if "content-disposition" in headers.keys():
            cdisp = headers["content-disposition"]
            file_names = re.findall("filename=(.+)", cdisp)
            if len(file_names) > 0:
                return file_names[0][0], file_names[0][1][1:]

        # Check content-type
        if "content-type" in headers.keys():
            ctype = headers["content-type"]
            if (not "text" in ctype) and (not "html" in ctype):
                return ctype.split("/")

    @classmethod
    def _download_bytes(cls, url: str):
        response = requests.get(url)
        if response.ok:
            filename = (
                cls._filename_from_headers(response.headers)
                or cls._filename_from_url(url)
                or ["download", None]
            )
            return filename, response.content

    def load(self):
        if validators.url(self.source):
            response = self._download_bytes(self.source)
            if response:
                self.__extension = response[0][1]
                self.__data = response[1]
        elif path.exists(self.source):
            basename = path.basename(self.source)
            self.__extension = path.splitext(basename)[1][1:]

            with open(self.source, "rb") as fp:
                self.__data = fp.read()
        else:
            pass  # TODO: Raise Exception

    def save(self, dest: str, add_extension: bool = True):
        if (
            len(path.splitext(dest)[1]) == 0
            and self.__extension != None
            and add_extension == True
        ):
            dest += self.__extension

        with open(dest, "wb") as fp:
            fp.write(self.__data)

        return dest


class Skin(_Resource):
    """
    Attributes:
        source (str): The source where the skin is located
        variant (str): The variant of skin (default to 'classic')
    """

    def __init__(
        self,
        source: str,
        variant: str,
        id: str = None,
        state: str = None,
        load: bool = True,
    ) -> None:
        super().__init__(source, load=load)
        self.__variant = variant
        self.__id = id
        self.__state = state

    @property
    def variant(self):
        return self.__variant

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    def __hash__(self) -> int:
        return hash((self.source, self.variant, self.data))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Skin):
            return hash(self) == hash(o)

        return False

    def __repr__(self) -> str:
        return f"Skin(source='{self.source}', variant='{self.variant}', id='{self.id}', state='{self.state}')"

    __str__ = __repr__


class Cape(_Resource):
    """
    Attributes:
        source (str): The source where the cape is located
    """

    def __init__(
        self, source: str, id: str = None, state: str = None, load: bool = True
    ) -> None:
        super().__init__(source, load=load)
        self.__id = id
        self.__state = state

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    def __hash__(self) -> int:
        return hash((self.source, self.data))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cape):
            return hash(self) == hash(o)

        return False

    def __repr__(self) -> str:
        return f"Cape(source='{self.source}', id='{self.id}', state='{self.state}')"

    __str__ = __repr__
