from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class LogRefItem(BaseModel):
    Source: str
    Identifier: str
    Attributes: Optional[List[str]] = None


@dataclass(frozen=True)
class LogItem(BaseModel):
    Code: str
    Message: str
    Refs: List[LogRefItem]


@dataclass(frozen=True)
class LogList(BaseModel):
    logs: Dict[str, LogItem]
