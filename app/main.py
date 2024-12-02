from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.api_v1.places.views import router as places_router
from app.api_v1.users.views import router as users_router
from app.api_v1.routes.views import router as routers_router
from app.api_v1.routes.views import review_router
from app.api_v1.users.user_manager import (
    auth_backend,
    current_active_user,
    UserManager,
    get_user_manager,
    fastapi_users,
)
from app.core.base import Base
from app.db.db_helper import db_helper
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.user import User
    from app.models.place import (
        Place,
        Tag,
    )
    from app.models.route import (
        Route,
        RoutePlace,
        RouteReview,
    )

    # Импортируем все модели перед созданием таблиц

    # async with db_helper.engine.begin() as conn:
    #     # Удаляем все таблицы
    #     # await conn.run_sync(Base.metadata.drop_all)
    #     # Создаем таблицы заново
    #     await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    lifespan=lifespan,
    title="TravelCraft",
    description="Сервис для путешественников",
    version="0.0.1",
    contact={
        "name": "HardLine89",
        "url": "https://github.com/HardLine89/TravelCraft",
        "email": "maggot8950@gmail.com",
    }
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api_v1/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api_v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api_v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api_v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api_v1/users",
    tags=["users"],
)

app.include_router(places_router, prefix="/api_v1")
app.include_router(users_router, prefix="/api_v1")
app.include_router(routers_router, prefix="/api_v1")
app.include_router(review_router, prefix="/api_v1")


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
