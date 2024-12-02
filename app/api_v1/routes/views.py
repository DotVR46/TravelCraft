from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.routes import crud
from app.db.db_helper import db_helper
from app.schemas.route import (
    RouteDetail,
    RouteCreate,
    RouteUpdate,
    RouteReviewUpdate,
    RouteReviewDetail,
    RouteReviewCreate,
)

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


review_router = APIRouter(tags=["Route Reviews"], prefix="/route-reviews")


@review_router.get(
    "/",
    response_model=list[RouteReviewDetail],
    description="Получить список всех отзывов о маршрутах.",
)
async def get_route_reviews(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_route_reviews(session=session)


@review_router.get(
    "/{review_id}",
    response_model=RouteReviewDetail,
    description="Получить отзыв о маршруте по id.",
)
async def get_route_review(
    review_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    review = await crud.get_route_review(session=session, review_id=review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отзыв не найден."
        )
    return review


@review_router.post(
    "/",
    response_model=RouteReviewDetail,
    status_code=status.HTTP_201_CREATED,
    description="Создать отзыв о маршруте.",
)
async def create_route_review(
    review_in: RouteReviewCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_route_review(session=session, review_in=review_in)


@review_router.put(
    "/{review_id}",
    response_model=RouteReviewUpdate,
    description="Обновить отзыв о маршруте по id.",
)
async def update_route_review(
    review_id: int,
    review_in: RouteReviewUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_route_review(
        session=session, review_id=review_id, review_in=review_in
    )


@review_router.delete(
    "/{review_id}",
    description="Удалить отзыв о маршруте по id.",
)
async def delete_route_review(
    review_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_route_review(session=session, review_id=review_id)
