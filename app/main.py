from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from fastapi_users.authentication import Authenticator
from fastapi_users.models import UP, ID
from sqlalchemy.exc import SQLAlchemyError

from app.api_v1.places.views import router as places_router
from app.api_v1.users.user_manager import (
    auth_backend,
    current_active_user,
    UserManager,
    get_user_manager, fastapi_users,
)
from app.core.base import Base
from app.db.db_helper import db_helper
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.place import (
        Place,
        Tag,
    )  # Импортируем все модели перед созданием таблиц

    async with db_helper.engine.begin() as conn:
        # Удаляем все таблицы
        # await conn.run_sync(Base.metadata.drop_all)
        # Создаем таблицы заново
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
