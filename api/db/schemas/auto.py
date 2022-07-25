from typing import Optional

from pydantic import BaseModel


class AutoBase(BaseModel):
    year: Optional[int]
    make: Optional[str]
    model: Optional[str] = None
    category: Optional[str] = None


# Properties to receive via API on creation
class AutoCreate(AutoBase):
    year: Optional[int]
    make: Optional[str]
    model: Optional[str] = None
    category: Optional[str] = None


# Properties to receive via API on update
class AutoUpdate(AutoBase):
    ...


# Additional properties to return via API
class Auto(AutoBase):
    ...
