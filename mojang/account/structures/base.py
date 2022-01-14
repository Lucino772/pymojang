import datetime as dt
from typing import NamedTuple, Tuple, Union


# Status check
class ServiceStatus(NamedTuple):
    """
    :var str name: The service name
    :var str status: The service status
    """

    name: str
    status: str


class StatusCheck(Tuple[ServiceStatus, ...]):
    def get(self, name: str) -> Union[None, ServiceStatus]:
        """Get service by name

        :param str name: The service name
        """
        service = list(filter(lambda s: s.name == name, self))
        if len(service) > 0:
            return service[0]


# UUID and Name
class UUIDInfo(NamedTuple):
    """
    :var str name: The user name
    :var str uuid: The user uuid
    :var bool legacy: Wether the account has migrated
    :var bool demo: Wether the account is demo
    """

    name: str
    uuid: str
    legacy: bool = False
    demo: bool = False


class NameInfo(NamedTuple):
    """
    :var str name: The player name
    :var datetime.datetime changed_to_at: When it's was changed to
    """

    name: str
    changed_to_at: dt.datetime


class NameInfoList(Tuple[NameInfo, ...]):
    @property
    def current(self) -> NameInfo:
        """Returns the most recent name"""
        if len(self) == 1:
            return self[0]

        _list = filter(lambda n: n.change_to_at is not None, self)
        return max(_list, key=lambda n: n.change_to_at)

    @property
    def first(self) -> NameInfo:
        """Returns the first name"""
        first = list(filter(lambda n: n.changed_to_at is None, self))
        return first[0]
