from pydantic import BaseModel
from typing import List


class PacketItem(BaseModel):
    packet_id: str
    src_pod: str
    dst_pod: str
    timestamp: str
    data_len: int


class PacketList(BaseModel):
    data: List[PacketItem]
