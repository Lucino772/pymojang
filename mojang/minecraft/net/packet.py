import typing as t
from dataclasses import dataclass


@dataclass
class Packet:
    packet_id: t.ClassVar[int] = -1
