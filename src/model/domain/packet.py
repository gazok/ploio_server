from pydantic import BaseModel
from typing import Dict


class PacketItem(BaseModel):
    Timestamp: str
    Source: str
    Destination: str
    Size: int
    Raw: str


class PacketList(BaseModel):
    packets: Dict[str, PacketItem]
