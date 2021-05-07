import datetime as dt
from dataclasses import dataclass, field
from typing import Tuple, Union
from .session import Skin, Cape


# Status check
@dataclass(frozen=True)
class ServiceStatus:
    name: str = field()
    status: str = field()

class StatusCheck(Tuple[ServiceStatus]):
    
    def get(self, name: str) -> Union[None, ServiceStatus]:
        service = list(filter(lambda s: s.name == name, self))
        if len(service) > 0:
            return service[0]

# UUID and Name
@dataclass(frozen=True)
class UUIDInfo:
    name: str = field()
    uuid: str = field()
    legacy: bool = field(default=False)
    demo: bool = field(default=False)

@dataclass(frozen=True)
class NameInfo:
    name: str = field()
    changed_to_at: dt.datetime = field()

class NameInfoList(Tuple[NameInfo]):
    
    @property
    def current(self) -> NameInfo:
        if len(self) == 1:
            return self[0]

        _list = filter(lambda n: n.change_to_at != None, self)
        return max(_list, key=lambda n: n.change_to_at)
    
    @property
    def first(self) -> Union[None, NameInfo]:
        first = list(filter(lambda n: n.changed_to_at == None, self))
        if len(first) > 0:
            return first[0]

## Profile
@dataclass
class UserProfile:
    name: str = field()
    uuid: str = field()
    is_legacy: bool = field()
    is_demo: bool = field()
    names: NameInfoList = field()
    skin: Skin = field()
    cape: Cape = field()
