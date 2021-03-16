from urllib.parse import urljoin

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
       