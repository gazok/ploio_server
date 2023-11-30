from pydantic import BaseModel
from typing import List


class NoticeItem(BaseModel):
    packet_id: str
    src_pod: str
    dst_pod: str
    timestamp: str
    data_len: int
    danger_degree: str
    danger_message: str


class NoticeList(BaseModel):
    data: List[NoticeItem]
