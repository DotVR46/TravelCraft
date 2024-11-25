from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import db_helper
from . import crud
from ...schemas.place import Place, PlaceCreate, PlaceUpdate

router = APIRouter(tags=["Places"], prefix="/places")


@router.get("/", response_model=list[Place], description="Получить список всех мест.")
async def get_places(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_places(session=session)


@router.get("/{place_id}", response_model=Place, description="Получить место по id.")
async def get_place(
    place_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_place(session=session, place_id=place_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Место не найдено."
        )
    return product


@router.post(
    "/",
    response_model=Place,
    status_code=status.HTTP_201_CREATED,
    description="Создать место.",
)
async def create_place(
    place_in: PlaceCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_place(session=session, place_in=place_in)


@router.put(
    "/{place_id}",
    response_model=Place,
    description="Обновить место по id.",
)
async def update_place(
    place_id: int,
    place_in: PlaceUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_place(
        session=session, place_id=place_id, place_in=place_in
    )


@router.delete(
    "/{place_id}",
    description="Удалить место по id.",
)
async def delete_place(
    place_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_place(session=session, place_id=place_id)
