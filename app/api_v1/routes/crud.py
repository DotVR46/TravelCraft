from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Route, RoutePlace
from app.schemas.route import RouteCreate, RouteUpdate


async def get_routes(session: AsyncSession) -> list[Route]:
    stmt = select(Route).options(joinedload(Route.places)).order_by(Route.id)
    result = await session.execute(stmt)
    routes = result.scalars().unique().all()
    return list(routes)


async def get_route(session: AsyncSession, route_id: int) -> Route | None:
    stmt = select(Route).where(Route.id == route_id).options(joinedload(Route.places))
    result = await session.execute(stmt)
    return result.scalars().unique().one_or_none()


async def create_route(
    session: AsyncSession, route_in: RouteCreate, author_id: int
) -> Route:
    # Создаем маршрут
    route = Route(**route_in.model_dump(exclude={"places"}), author_id=author_id)
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
