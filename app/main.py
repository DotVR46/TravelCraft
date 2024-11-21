from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.api_v1.places.views import router as places_router
from app.core.base import Base
from app.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.place import (
        Place,
        Tag,
    )  # Импортируем все модели перед созданием таблиц

    async with db_helper.engine.begin() as conn:
        # Удаляем все таблицы
        await conn.run_sync(Base.metadata.drop_all)
        # Создаем таблицы заново
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(places_router, prefix="/api_v1/v1")
