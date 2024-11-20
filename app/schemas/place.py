from pydantic import BaseModel


class PlaceBase(BaseModel):
    name: str
    description: str


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        from_attributes = True
