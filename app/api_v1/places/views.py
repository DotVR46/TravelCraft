from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import db_helper
from . import crud
from ...schemas.place import PlaceResponse

router = APIRouter(tags=["Products"], prefix="/places")


@router.get("/", response_model=list[PlaceResponse], description="Получить список всех мест.")
async def get_places(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.get("/{place_id}", response_model=PlaceResponse, description="Получить место по id.")
async def get_place(
    place_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud.get_product(session=session, product_id=place_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Место не найдено"
        )
    return product
