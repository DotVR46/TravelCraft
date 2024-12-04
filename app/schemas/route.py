from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

from app.schemas.place import Place


class RouteBase(BaseModel):
    title: str
    description: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    photo: HttpUrl | None


class RouteCreate(RouteBase):
    author_id: int
    places: List[int]  # IDs мест, включенных в маршрут


class RouteDetail(RouteBase):
    id: int
    author_id: int
    places: List[Place]

    class Config:
        from_attributes = True


class RouteUpdate(RouteBase):
    title: Optional[str] = Field(None, max_length=255, description="Название маршрута")
    description: Optional[str] = Field(None, description="Описание маршрута")
    places: Optional[list[int]] = Field(
        None, description="Список ID мест, которые входят в маршрут"
    )

    class Config:
        from_attributes = True


class RouteReviewBase(BaseModel):
    text: str
    rating: int = Field(..., ge=1, le=5)  # Рейтинг от 1 до 5
    created_at: Optional[datetime] = None


class RouteReviewCreate(RouteReviewBase):
    route_id: int  # ID маршрута, к которому относится отзыв
    author_id: int


class RouteReviewDetail(RouteReviewBase):
    id: int
    author_id: int  # ID автора отзыва
    route_id: int  # ID маршрута

    class Config:
        from_attributes = True


class RouteReviewUpdate(RouteReviewBase):
    rating: Optional[float] = Field(
        None, ge=0, le=5, description="Оценка маршрута от 0 до 5"
    )
    content: Optional[str] = Field(None, description="Текстовый отзыв о маршруте")

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
