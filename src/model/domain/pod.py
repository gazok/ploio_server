from pydantic import BaseModel
from typing import Dict, List


class PodItem(BaseModel):
    id: str
    name: str
    name_space: str
    ip: str
    danger_degree: str
    message: str


class PodList(BaseModel):
    pods: List[PodItem]
