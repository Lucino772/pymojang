from dataclasses import dataclass

from mojang.minecraft.net.packet import Packet


@dataclass
class PingRequest(Packet):
    packet_id = 0x01
