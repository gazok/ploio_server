from pydantic import BaseModel
from typing import List


class ModuleItem(BaseModel):
    GUID: str
    Name: str
    Description: str
    Status: str


class ModuleList(BaseModel):
    modules: List[ModuleItem]
