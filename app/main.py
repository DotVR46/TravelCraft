from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api_v1.places.views import router as places_router
from app.core.base import Base
from app.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(places_router, prefix="/api_v1/v1")
