import datetime as dt
from typing import Callable, NamedTuple, Optional, Tuple, Union


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

        return None


# UUID and Name
class NameInfo(NamedTuple):
    """
    :var str name: The player name
    :var datetime.datetime changed_to_at: When it's was changed to
    """

    name: str
    changed_to_at: Optional[dt.datetime]


class NameInfoList(Tuple[NameInfo, ...]):
    @property
    def current(self) -> NameInfo:
        """Returns the most recent name"""
        if len(self) == 1:
            return self[0]

        _max = self[0]
        for n in self[1:]:
            if (n.changed_to_at is not None) and (
                _max.changed_to_at is None
                or n.changed_to_at > _max.changed_to_at
            ):
                _max = n

        return _max

    @property
    def first(self) -> NameInfo:
        """Returns the first name"""
        first = list(filter(lambda n: n.changed_to_at is None, self))
        return first[0]
