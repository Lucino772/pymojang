import datetime as dt
from typing import Iterator, NamedTuple, Union

from .session import Cape, Skin


# Status check
class ServiceStatus(NamedTuple):
    """
    Attributes:
        name (str): The service name
        status (str): The service status
    """
    name: str
    status: str


class StatusCheck(tuple):
    
    def get(self, name: str) -> Union[None, 'ServiceStatus']:
        """Get service by name

        Args:
            name (str): The service name
        
        Returns:
            ServiceStatus
        """
        service = list(filter(lambda s: s.name == name, self))
        if len(service) > 0:
            return service[0]

    def __getitem__(self, x) -> ServiceStatus:
        return super().__getitem__(x)

    def __iter__(self) -> Iterator['ServiceStatus']:
        return super().__iter__()


# UUID and Name
class UUIDInfo(NamedTuple):
    """
    Attributes:
        name (str): The user name
        uuid (str): The user uuid
        legacy (bool): Wether the account has migrated
        demo (bool): Wether the account is demo
    """
    name: str
    uuid: str
    legacy: bool = False
    demo: bool = False


class NameInfo(NamedTuple):
    """
    Attributes:
        name (str): The player name
        changed_to_at (dt.datetime): When it's was changed to
    """
    name: str
    changed_to_at: dt.datetime


class NameInfoList(tuple):

    @property
    def current(self) -> NameInfo:
        """Returns the most recent name"""
        if len(self) == 1:
            return self[0]

        _list = filter(lambda n: n.change_to_at != None, self)
        return max(_list, key=lambda n: n.change_to_at)
    
    @property
    def first(self) -> NameInfo:
        """Returns the first name"""
        first = list(filter(lambda n: n.changed_to_at == None, self))
        return first[0]

    def __getitem__(self, x) -> NameInfo:
        return super().__getitem__(x)

    def __iter__(self) -> Iterator['NameInfo']:
        return super().__iter__()


## Profile
class UserProfile(NamedTuple):
    """
    Attributes:
        name (str): The user name
        uuid (str): The user uuid
        is_legacy (bool): Wether the account has migrated
        is_demo (bool): Wether the account is demo
        names (NameInfoList): The user name history
        skin (Skin): The user skin
        cape (Cape): The user cape
    """
    name: str
    uuid: str
    is_legacy: bool
    is_demo: bool
    names: NameInfoList
    skin: Skin
    cape: Cape
