from typing import List
from .base import NameInfoList
from .session import Skin, Cape


class BaseUserProfile:
    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: NameInfoList,
    ) -> None:
        self.__name = name
        self.__uuid = uuid
        self.__is_legacy = is_legacy
        self.__is_demo = is_demo
        self.__names = names

    def __hash__(self) -> int:
        return hash(
            (
                self.__name,
                self.__uuid,
                self.__is_legacy,
                self.__is_demo,
                self.__names,
            )
        )

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BaseUserProfile):
            return hash(self) == hash(o)

        return False

    @property
    def name(self):
        return self.__name

    @property
    def uuid(self):
        return self.__uuid

    @property
    def is_legacy(self):
        return self.__is_legacy

    @property
    def is_demo(self):
        return self.__is_demo

    @property
    def names(self):
        return self.__names


class UnauthenticatedProfile(BaseUserProfile):
    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: NameInfoList,
        skin: Skin,
        cape: Cape,
    ) -> None:
        super().__init__(name, uuid, is_legacy, is_demo, names)
        self.__skin = skin
        self.__cape = cape

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.uuid,
                self.is_legacy,
                self.is_demo,
                self.names,
                self.__skin,
                self.__cape,
            )
        )

    @property
    def skin(self):
        return self.__skin

    @property
    def cape(self):
        return self.__cape

    def __repr__(self) -> str:
        return f"UnauthenticatedProfile(name='{self.name}', uuid='{self.uuid}', is_legacy={self.is_legacy}, is_demo={self.is_demo}, names={self.names}, skin={repr(self.skin)}, cape={repr(self.cape)})"


class AuthenticatedUserProfile(BaseUserProfile):
    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: NameInfoList,
        skins: List[Skin],
        capes: List[Cape],
    ) -> None:
        super().__init__(name, uuid, is_legacy, is_demo, names)
        self.__skins = skins
        self.__capes = capes

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.uuid,
                self.is_legacy,
                self.is_demo,
                self.names,
                self.__skins,
                self.__capes,
            )
        )

    @property
    def skins(self):
        return self.__skins

    @property
    def capes(self):
        return self.__capes

    def __repr__(self) -> str:
        return f"AuthenticatedProfile(name='{self.name}', uuid='{self.uuid}', is_legacy={self.is_legacy}, is_demo={self.is_demo}, names={self.names}, skins=[{len(self.__skins)}], cape=[{len(self.capes)}])"
