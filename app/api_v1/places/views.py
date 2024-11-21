from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import db_helper
from . import crud
from ...schemas.place import PlaceResponse, PlaceCreate

router = APIRouter(tags=["Products"], prefix="/places")


@router.get(
    "/", response_model=list[PlaceResponse], description="Получить список всех мест."
)
async def get_places(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_place(session=session)


@router.get(
    "/{place_id}", response_model=PlaceResponse, description="Получить место по id."
)
async def get_place(
    place_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_places(session=session, place_id=place_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Место не найдено"
        )
    return product


@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
async def create_place(
    place_in: PlaceCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_place(session=session, place_in=place_in)
