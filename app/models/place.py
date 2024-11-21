from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
import datetime

from app.core.base import Base


# Определяем модель Tag
class Tag(Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Связь с Place через place_tags
    places = relationship("Place", secondary="place_tags", back_populates="tags")


# Таблица для связи Place и Tag
place_tags = Table(
    "place_tags",
    Base.metadata,
    Column("place_id", Integer, ForeignKey("places.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Place(Base):

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    rating = Column(Float, default=0)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow
    )

    # Связи
    tags = relationship("Tag", secondary=place_tags, back_populates="places")
    # creator_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"<Place(name={self.name}, rating={self.rating})>"
