from pydantic import BaseModel
from typing import List


class ModuleItem(BaseModel):
    guid: str
    name: str
    description: str
    status: str


class ModuleList(BaseModel):
    modules: List[ModuleItem]
