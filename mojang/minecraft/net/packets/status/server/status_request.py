from dataclasses import dataclass

from mojang.minecraft.net.packet import Packet


@dataclass
class StatusRequest(Packet):
    packet_id = 0x00
