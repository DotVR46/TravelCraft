from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.place import Place, Tag
from app.schemas.place import PlaceCreate, PlaceUpdate


async def get_places(session: AsyncSession) -> list[Place]:
    stmt = (
        select(Place)
        .options(joinedload(Place.tags))  # Предзагрузка связанных тегов
        .order_by(Place.id)
    )
    result: Result = await session.execute(stmt)
    places = result.scalars().unique().all()
    return list(places)


async def get_place(session: AsyncSession, place_id: int) -> Place | None:
    stmt = (
        select(Place)
        .where(Place.id == place_id)
        .options(joinedload(Place.tags))  # Предзагрузка тегов
    )
    result = await session.execute(stmt)
    return result.scalars().unique().one_or_none()


async def create_place(session: AsyncSession, place_in: PlaceCreate) -> Place:
    # Создаем место из переданных данных
    place = Place(**place_in.model_dump(exclude={"tags"}))

    # Обрабатываем теги
    tags = []
    for tag_in in place_in.tags:  # Массив тегов из запроса
        # Проверяем, существует ли тег
        existing_tag = await session.execute(
            select(Tag).filter(Tag.name == tag_in.name)
        )
        existing_tag = existing_tag.scalar_one_or_none()

        if existing_tag:  # Если тег существует, добавляем его
            tags.append(existing_tag)
        else:  # Если тег не существует, создаем новый и добавляем его
            new_tag = Tag(name=tag_in.name)
            session.add(new_tag)
            tags.append(new_tag)

    # Привязываем теги к месту
    place.tags = tags

    # Добавляем место в базу данных
    session.add(place)
    await session.commit()

    # Не забываем обновить объект после коммита, чтобы получить id
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
