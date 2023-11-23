from pydantic import BaseModel
from typing import List


class PacketItem(BaseModel):
    src_pod: str
    dst_pod: str
    timestamp: str
    data_len: int


class PacketList(BaseModel):
    data: List[PacketItem]
