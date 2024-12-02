from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.place import Place


class RouteBase(BaseModel):
    title: str
    description: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RouteCreate(RouteBase):
    places: List[int]  # IDs мест, включенных в маршрут


class RouteDetail(RouteBase):
    id: int
    author_id: int
    places: List[Place]

    class Config:
        from_attributes = True


class RouteReviewBase(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)  # Рейтинг от 1 до 5
    created_at: Optional[datetime] = None


class RouteReviewCreate(RouteReviewBase):
    route_id: int  # ID маршрута, к которому относится отзыв


class RouteReviewDetail(RouteReviewBase):
    id: int
    author_id: int  # ID автора отзыва
    route_id: int  # ID маршрута

    class Config:
        from_attributes = True


class RoutePlaceBase(BaseModel):
    route_id: int
    place_id: int
    order: int  # Порядок места в маршруте


class RoutePlaceCreate(RoutePlaceBase):
    pass


class RoutePlaceDetail(RoutePlaceBase):
    id: int

    class Config:
        from_attributes = True
