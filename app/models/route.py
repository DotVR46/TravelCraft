import enum
import datetime
from sqlalchemy import String, Text, ForeignKey, Enum, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.base import Base


class RouteStatus(enum.Enum):
    PLANNED = "planned"  # Планируемый маршрут
    COMPLETED = "completed"  # Завершенный маршрут


class Route(Base):
    """
    Маршрут
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # Название маршрута
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # Описание маршрута
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )  # Автор маршрута
    status: Mapped[RouteStatus] = mapped_column(
        Enum(RouteStatus), default=RouteStatus.PLANNED, nullable=False
    )  # Статус маршрута
    photo: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.datetime.now
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )
    # Связи
    author: Mapped["User"] = relationship(
        "User", back_populates="routes"
    )  # Ссылка на пользователя
    places: Mapped[list["RoutePlace"]] = relationship(
        "RoutePlace", back_populates="route", cascade="all, delete-orphan"
    )  # Места маршрута
    reviews: Mapped[list["RouteReview"]] = relationship(
        "RouteReview", back_populates="route", cascade="all, delete-orphan"
    )  # Отзывы

    def __repr__(self):
        return f"<Route(name={self.name}, status={self.status})>"


class RoutePlace(Base):
    """
    Место в маршруте
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id"), nullable=False
    )  # Ссылка на маршрут
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id"), nullable=False
    )  # Ссылка на место
    order: Mapped[int] = mapped_column(nullable=False)  # Порядок посещения

    # Связи
    route: Mapped["Route"] = relationship(
        "Route", back_populates="places"
    )  # Ссылка на маршрут
    place: Mapped["Place"] = relationship(
        "Place", back_populates="route_places"
    )  # Ссылка на место

    def __repr__(self):
        return f"<RoutePlace(route_id={self.route_id}, place_id={self.place_id}, order={self.order})>"


class RouteReview(Base):
    """
    Отзыв о маршруте
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id"), nullable=False
    )  # Ссылка на маршрут
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )  # Автор отзыва
    text: Mapped[str] = mapped_column(Text, nullable=False)  # Текст отзыва
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # Рейтинг (1-5)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.datetime.now
    )

    # Связи
    route: Mapped["Route"] = relationship(
        "Route", back_populates="reviews"
    )  # Ссылка на маршрут
    author: Mapped["User"] = relationship("User")  # Ссылка на пользователя

    def __repr__(self):
        return f"<RouteReview(route_id={self.route_id}, rating={self.rating})>"
