from pydantic import BaseModel
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PacketItem(BaseModel):
    src_pod: str
    dst_pod: str
    timestamp: str
    data_len: int


@dataclass(frozen=True)
class PacketList(BaseModel):
    data: List[PacketItem]
