from .web import Downloadable


class Skin(Downloadable):

    def __init__(self, source: str, variant: str='classic'):
        super().__init__(source)
        self.__variant = variant

    @property
    def variant(self):
        return self.__variant
