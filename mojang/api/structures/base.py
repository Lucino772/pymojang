import datetime as dt
from typing import NamedTuple, Optional, Tuple, Union


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
