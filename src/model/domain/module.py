from pydantic import BaseModel
from typing import List


class ModuleItem(BaseModel):
    GUID: str
    Name: str
    Description: str


class ModuleList(BaseModel):
    data: List[ModuleItem]
