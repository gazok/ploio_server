from pydantic import BaseModel
from typing import Dict, List, Optional


class LogRefItem(BaseModel):
    Source: str
    Identifier: str
    Attributes: Optional[List[str]] = None


class LogItem(BaseModel):
    Code: str
    Message: str
    Refs: List[LogRefItem]


class LogList(BaseModel):
    logs: Dict[str, LogItem]
