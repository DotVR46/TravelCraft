from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Route, RoutePlace
from app.models.route import RouteReview
from app.schemas.route import (
    RouteCreate,
    RouteUpdate,
    RouteReviewCreate,
    RouteReviewUpdate,
)


# CRUD для маршрутов


async def get_routes(session: AsyncSession) -> list[Route]:
    stmt = select(Route).options(joinedload(Route.places)).order_by(Route.id)
    result = await session.execute(stmt)
    routes = result.scalars().unique().all()
    return list(routes)


async def get_route(session: AsyncSession, route_id: int) -> Route | None:
    stmt = select(Route).where(Route.id == route_id).options(joinedload(Route.places))
    result = await session.execute(stmt)
    return result.scalars().unique().one_or_none()


async def create_route(session: AsyncSession, route_in: RouteCreate) -> Route:
    # Создаем маршрут
    route = Route(**route_in.model_dump(exclude={"places"}))
    session.add(route)

    # Привязываем места к маршруту
    for order, place_id in enumerate(route_in.places):
        route_place = RoutePlace(route_id=route.id, place_id=place_id, order=order)
        session.add(route_place)

    await session.commit()
    await session.refresh(route)  # Обновляем объект для получения данных
    return route


async def update_route(
    session: AsyncSession, route_id: int, route_in: RouteUpdate, partial: bool = False
) -> Type[Route] | None:
    route = await session.get(Route, route_id)
    if not route:
        return None

    for name, value in route_in.model_dump(exclude_unset=partial).items():
        setattr(route, name, value)

    await session.commit()
    await session.refresh(route)
    return route


async def delete_route(session: AsyncSession, route_id: int) -> Type[Route] | None:
    route = await session.get(Route, route_id)
    if not route:
        return None
    await session.delete(route)
    await session.commit()
    return route


# CRUD для отзывов


async def get_route_review(session: AsyncSession, review_id: int) -> Route | None:
    stmt = select(RouteReview).where(RouteReview.id == review_id)
    result = await session.execute(stmt)
    return result.scalars().unique().one_or_none()


async def get_route_reviews(session: AsyncSession, route_id: int) -> list[RouteReview]:
    stmt = (
        select(RouteReview)
        .where(RouteReview.route_id == route_id)
        .order_by(RouteReview.id)
    )
    result = await session.execute(stmt)
    reviews = result.scalars().unique().all()
    return list(reviews)


async def create_route_review(
    session: AsyncSession, review_in: RouteReviewCreate
) -> RouteReview:
    review = RouteReview(**review_in.model_dump())
    session.add(review)
    await session.commit()
    # await session.refresh(review)
    return review


async def update_route_review(
    session: AsyncSession,
    review_id: int,
    review_in: RouteReviewUpdate,
    partial: bool = False,
) -> Type[RouteReview] | None:
    review = await session.get(RouteReview, review_id)
    if not review:
        return None

    for name, value in review_in.model_dump(exclude_unset=partial).items():
        setattr(review, name, value)

    await session.commit()
    # await session.refresh(review)
    return review


async def delete_route_review(
    session: AsyncSession, review_id: int
) -> Type[RouteReview] | None:
    review = await session.get(RouteReview, review_id)
    if not review:
        return None
    await session.delete(review)
    await session.commit()
    return review


# CRUD для привязки мест к маршрутам


async def get_route_places(session: AsyncSession, route_id: int) -> list[RoutePlace]:
    stmt = (
        select(RoutePlace)
        .where(RoutePlace.route_id == route_id)
        .order_by(RoutePlace.order)
    )
    result = await session.execute(stmt)
    places = result.scalars().unique().all()
    return list(places)


async def add_place_to_route(
    session: AsyncSession, route_id: int, place_id: int, order: int
) -> RoutePlace:
    route_place = RoutePlace(route_id=route_id, place_id=place_id, order=order)
    session.add(route_place)
    await session.commit()
    # await session.refresh(route_place)
    return route_place


async def remove_place_from_route(
    session: AsyncSession, route_place_id: int
) -> Type[RoutePlace] | None:
    route_place = await session.get(RoutePlace, route_place_id)
    if not route_place:
        return None
    await session.delete(route_place)
    await session.commit()
    return route_place
