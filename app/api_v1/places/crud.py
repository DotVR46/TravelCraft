from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.place import Place
from app.schemas.place import PlaceCreate, PlaceUpdate


async def get_place(session: AsyncSession) -> list[Place]:
    stmt = select(Place).order_by(Place.id)
    result: Result = await session.execute(stmt)
    places = result.scalars().all()
    return list(places)


async def get_places(session: AsyncSession, place_id: int) -> Place | None:
    return await session.get(Place, place_id)


async def create_place(session: AsyncSession, place_in: PlaceCreate) -> Place:
    place = Place(**place_in.model_dump())
    session.add(place)
    await session.commit()
    # await session.refresh(place)
    return place


async def update_place(
    session: AsyncSession, place_id: int, place_in: PlaceUpdate, partial: bool = False
) -> Place | None:
    place = await session.get(Place, place_id)
    for name, value in place_in.model_dump(exclude_unset=partial).items():
        setattr(place, name, value)
    await session.commit()
    return place


async def delete_place(session: AsyncSession, place_id: int) -> Place | None:
    place = await session.get(Place, place_id)
    await session.delete(place)
    await session.commit()
    return place
