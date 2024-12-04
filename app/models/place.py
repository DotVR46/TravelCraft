from typing import Optional

from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Table, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
import datetime

from app.core.base import Base

place_tags = Table(
    "place_tags",
    Base.metadata,
    Column("place_id", Integer, ForeignKey("places.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


# Определяем модель Tag
class Tag(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Связь с местами
    places: Mapped[list["Place"]] = relationship(
        "Place", secondary=place_tags, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(name={self.name})>"


# Таблица для связи Place и Tag


class Place(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    photo: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
    route_places: Mapped[list["RoutePlace"]] = relationship(
        "RoutePlace", back_populates="place", cascade="all, delete-orphan"
    )

    # Связи
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=place_tags, back_populates="places"
    )

    def __repr__(self):
        return f"<Place(name={self.name}, rating={self.rating})>"
