from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.routes import crud
from app.db.db_helper import db_helper
from app.schemas.route import RouteDetail, RouteCreate, RouteUpdate

router = APIRouter(tags=["Routes"], prefix="/routes")


@router.get(
    "/", response_model=list[RouteDetail], description="Получить список всех маршрутов."
)
async def get_routes(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_routes(session=session)


@router.get(
    "/{route_id}", response_model=RouteDetail, description="Получить маршрут по id."
)
async def get_route(
    route_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    route = await crud.get_route(session=session, route_id=route_id)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не найден."
        )
    return route


@router.post(
    "/",
    response_model=RouteCreate,
    status_code=status.HTTP_201_CREATED,
    description="Создать маршрут.",
)
async def create_route(
    route_in: RouteCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_route(session=session, route_in=route_in)


@router.put(
    "/{route_id}",
    response_model=RouteUpdate,
    description="Обновить маршрут по id.",
)
async def update_route(
    route_id: int,
    route_in: RouteUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_route(
        session=session, route_id=route_id, route_in=route_in
    )


@router.delete(
    "/{route_id}",
    description="Удалить маршрут по id.",
)
async def delete_route(
    route_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_route(session=session, route_id=route_id)
