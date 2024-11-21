from typing import Optional

from pydantic import BaseModel


class PlaceBase(BaseModel):
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    address: Optional[str]


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]


class PlaceResponse(PlaceBase):
    id: int
    rating: float
    likes: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
