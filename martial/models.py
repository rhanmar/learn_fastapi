from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel
from enum import Enum


class Type(str, Enum):
    wrestling = "wrestling"
    kick = "kick"
    mixed = "mixed"


class Style(BaseModel):
    id: Optional[int]
    name: str
    type: Type


class Artist(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    styles: List[Style]
