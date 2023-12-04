from pydantic import BaseModel
from typing import List
from datetime import datetime

class PacketItem(BaseModel):
    packet_id: str
    src_pod: str
    dst_pod: str
    timestamp: datetime
    data_len: int


class PacketList(BaseModel):
    packets: List[PacketItem]
