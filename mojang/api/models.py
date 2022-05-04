import os
import re
from typing import Optional
from urllib.parse import urlparse

import requests
import validators
from requests.structures import CaseInsensitiveDict


class _Resource:
    """Base class for downloadable resources

    :var str source: The source where the skin is located
    :var bytes data: Content of the resources in bytes
    :var str extension: The type of file, if detected
    """

    def __init__(self, source: str, load: bool = True) -> None:
        self.__source = source
        self.__data = bytes()
        self.__extension = None

        if load is True:
            self.load()

    @property
    def source(self) -> str:
        return self.__source

    @property
    def data(self) -> bytes:
        return self.__data

    @property
    def extension(self) -> Optional[str]:
        return self.__extension

    @classmethod
    def _filename_from_url(cls, url: str):
        url_path = urlparse(url).path
        match = re.match(
            r"^([\w,\s-]+)\.([A-Za-z]{3})$", os.path.basename(url_path)
        )
        if match:
            return match.groups()

    @classmethod
    def _filename_from_headers(cls, headers: CaseInsensitiveDict):
        # Check content-disposition
        if "content-disposition" in headers.keys():
            cdisp = headers["content-disposition"]
            file_names = re.findall("filename=(.+)", cdisp)
            if len(file_names) > 0:
                return file_names[0][0], file_names[0][1][1:]

        # Check content-type
        if "content-type" in headers.keys():
            ctype = headers["content-type"]
            if ("text" not in ctype) and ("html" not in ctype):
                return ctype.split("/")

    @classmethod
    def _download_bytes(cls, url: str):
        response = requests.get(url)
        if response.ok:
            filename = (
                cls._filename_from_url(url)
                or cls._filename_from_headers(response.headers)
                or ["download", None]
            )
            return filename, response.content

    def load(self):
        """Load data from the source"""
        if validators.url(self.source):
            response = self._download_bytes(self.source)
            if response:
                self.__extension = response[0][1]
                self.__data = response[1]
        elif os.path.exists(self.source):
            basename = os.path.basename(self.source)
            self.__extension = os.path.splitext(basename)[1][1:]

            with open(self.source, "rb") as fp:
                self.__data = fp.read()
        else:
            pass  # TODO: Raise Exception

    def save(self, dest: str, add_extension: bool = True):
        """Save resource in a file"""
        if (
            len(os.path.splitext(dest)[1]) == 0
            and self.__extension is not None
            and add_extension is True
        ):
            dest += "." + self.__extension

        with open(dest, "wb") as fp:
            fp.write(self.__data)

        return dest


class Skin(_Resource):
    """
    :var str variant: The variant of skin (default to 'classic')
    :var str id: The id of the skin
    :var str state: The state of the skin
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
    def variant(self) -> str:
        return self.__variant

    @property
    def id(self) -> Optional[str]:
        return self.__id

    @property
    def state(self) -> Optional[str]:
        return self.__state

    def __hash__(self) -> int:
        return hash(
            (self.source, self.id, self.state, self.variant, self.data)
        )

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Skin):
            return hash(self) == hash(o)

        return False

    def __repr__(self) -> str:
        return f"Skin(source='{self.source}', variant='{self.variant}', id='{self.id}', state='{self.state}')"

    __str__ = __repr__


class Cape(_Resource):
    """
    :var str id: The id of the cape
    :var str state: The state of the cape
    """

    def __init__(
        self, source: str, id: str = None, state: str = None, load: bool = True
    ) -> None:
        super().__init__(source, load=load)
        self.__id = id
        self.__state = state

    @property
    def id(self) -> Optional[str]:
        return self.__id

    @property
    def state(self) -> Optional[str]:
        return self.__state

    def __hash__(self) -> int:
        return hash((self.source, self.id, self.state, self.data))

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Cape):
            return hash(self) == hash(o)

        return False

    def __repr__(self) -> str:
        return f"Cape(source='{self.source}', id='{self.id}', state='{self.state}')"

    __str__ = __repr__
