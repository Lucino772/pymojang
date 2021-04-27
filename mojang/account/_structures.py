import datetime as dt
from typing import NamedTuple, Tuple, Union

# Status check
class ServiceStatus(NamedTuple):
    name: str
    status: str

class StatusCheck(Tuple[ServiceStatus]):
    
    def get(self, name: str) -> Union[None, ServiceStatus]:
        service = list(filter(lambda s: s.name == name, self))
        if len(service) > 0:
            return service[0]

# UUID and Name
class UUIDInfo(NamedTuple):
    name: str
    uuid: str
    legacy: bool = False
    demo: bool = False

class NameInfo(NamedTuple):
    name: str
    changed_to_at: dt.datetime

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
