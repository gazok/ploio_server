from pydantic import BaseModel
from dataclasses import dataclass
from typing import List


class LogItem(BaseModel):
    packet_id: str
    src_pod: str
    dst_pod: str
    timestamp: str
    data_len: int
    danger_degree: str
    danger_message: str


class LogList(BaseModel):
    logs: List[LogItem]
