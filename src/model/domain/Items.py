from pydantic import BaseModel
from typing import Dict, List, Optional


class PacketItem(BaseModel):
    Timestamp: str
    Source: str
    Destination: str
    Size: int
    Raw: str


class PacketList(BaseModel):
    packets: Dict[str, PacketItem]


class PodList(BaseModel):
    Name: str
    Namespace: str
    State: str
    CreatedAt: str
    Network: List[str]


class PodItem(BaseModel):
    pods: Dict[str, PodList]


class LogRefItem(BaseModel):
    Source: str
    Identifier: str
    Attributes: Optional[List[str]] = None


class LogItem(BaseModel):
    Code: str
    Message: str
    Refs: List[LogRefItem]


class LogList(BaseModel):
    logs: Dict[str, LogItem]
