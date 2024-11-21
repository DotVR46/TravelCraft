from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import db_helper
from . import crud

from app.schemas.place import Place

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Place])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)
