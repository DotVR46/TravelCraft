from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.place import Place
from app.schemas.place import PlaceCreate


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
