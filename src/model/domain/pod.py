from pydantic import BaseModel
from typing import Dict, List


class PodList(BaseModel):
    Name: str
    Namespace: str
    State: str
    CreatedAt: str
    Network: List[str]


class PodItem(BaseModel):
    pods: Dict[str, PodList]
