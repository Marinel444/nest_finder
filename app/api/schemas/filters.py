from pydantic import BaseModel
from datetime import datetime


class PurposeRead(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class PropertySubtypeRead(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class PropertyTypeRead(BaseModel):
    id: int
    code: str
    name: str
    created_at: datetime
    subtypes: list[PropertySubtypeRead] = []

    class Config:
        orm_mode = True
