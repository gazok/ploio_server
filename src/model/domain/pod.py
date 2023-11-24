from pydantic import BaseModel
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PodItem(BaseModel):
    id: str
    name: str
    name_space: str
    ip: str
    danger_degree: str
    message: str


@dataclass(frozen=True)
class PodList(BaseModel):
    pods: List[PodItem]
