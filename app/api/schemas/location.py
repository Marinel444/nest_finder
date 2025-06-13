from pydantic import BaseModel
from datetime import datetime


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int
    created_at: datetime


class CityBase(BaseModel):
    name: str
    country_id: int


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    created_at: datetime
