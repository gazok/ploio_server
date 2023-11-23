from pydantic import BaseModel
from typing import Dict, List


class PodItem(BaseModel):
    Name: str
    Namespace: str
    State: str
    CreatedAt: str
    Network: List[str]


class PodList(BaseModel):
    pods: Dict[str, PodItem]
