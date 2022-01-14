from typing import List, Optional
from .base import NameInfoList
from .session import Skin, Cape


class BaseUserProfile:
    """
    :var str name: The user name
    :var str uuid: The user uuid
    :var bool is_legacy: Wether the account has migrated
    :var bool is_demo: Wether the account is demo
    :var NameInfoList names: The user name history
    """

    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: Optional[NameInfoList],
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
    def name(self) -> str:
        return self.__name

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def is_legacy(self) -> bool:
        return self.__is_legacy

    @property
    def is_demo(self) -> bool:
        return self.__is_demo

    @property
    def names(self) -> Optional[NameInfoList]:
        return self.__names


class UnauthenticatedProfile(BaseUserProfile):
    """
    :var Skin skin: The active user skin
    :var Cape cape: The active user cape
    """

    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: Optional[NameInfoList],
        skin: Optional[Skin],
        cape: Optional[Cape],
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
    def skin(self) -> Optional[Skin]:
        return self.__skin

    @property
    def cape(self) -> Optional[Cape]:
        return self.__cape

    def __repr__(self) -> str:
        return f"UnauthenticatedProfile(name='{self.name}', uuid='{self.uuid}', is_legacy={self.is_legacy}, is_demo={self.is_demo}, names={self.names}, skin={repr(self.skin)}, cape={repr(self.cape)})"


class AuthenticatedUserProfile(BaseUserProfile):
    """
    :var List[Skin] skins: All the skins of the user
    :var List[Cape] capes: All the capes of the user
    """

    def __init__(
        self,
        name: str,
        uuid: str,
        is_legacy: bool,
        is_demo: bool,
        names: Optional[NameInfoList],
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
    def skins(self) -> List[Skin]:
        return self.__skins

    @property
    def capes(self) -> List[Cape]:
        return self.__capes

    def __repr__(self) -> str:
        return f"AuthenticatedProfile(name='{self.name}', uuid='{self.uuid}', is_legacy={self.is_legacy}, is_demo={self.is_demo}, names={self.names}, skins=[{len(self.__skins)}], cape=[{len(self.capes)}])"
