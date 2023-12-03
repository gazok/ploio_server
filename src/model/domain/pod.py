from pydantic import BaseModel
from typing import List


class PodItem(BaseModel):
    id: str
    name: str
    name_space: str
    type: str
    ip: str
    danger_degree: str
    danger_message: str


class PodList(BaseModel):
    pods: List[PodItem]
