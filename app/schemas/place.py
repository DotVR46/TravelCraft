from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class TagCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class TagResponse(TagCreate):
    id: int
    name: str

    class Config:
        from_attributes = True


class PlaceBase(BaseModel):
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    address: Optional[str]
    photo: HttpUrl | None


class PlaceCreate(PlaceBase):
    tags: Optional[List[TagCreate]]


class PlaceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]


class Place(PlaceBase):
    id: int
    rating: float
    likes: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse]
    photo: HttpUrl | None

    class Config:
        from_attributes = True
