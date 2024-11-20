from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.place import Place
from app.schemas.place import PlaceCreate, Place

router = APIRouter()


# Получить все места
@router.get("/places", response_model=list[Place])
async def get_places(session: AsyncSession = Depends(AsyncSessionLocal)):
    result = await session.execute(select(Place))
    return result.scalars().all()


# Создать место
@router.post("/places", response_model=Place)
async def create_place(
    place: PlaceCreate, session: AsyncSession = Depends(AsyncSessionLocal)
):
    db_place = Place(name=place.name, description=place.description)
    session.add(db_place)
    await session.commit()
    return db_place
