from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    JWTStrategy,
    AuthenticationBackend,
    CookieTransport,
)
from fastapi_users.manager import BaseUserManager, UUIDIDMixin
from typing import Optional
from app.db.user_db import get_user_db
from app.models.user import User
from fastapi import Depends, Request
from app.schemas.user import UserRead, UserCreate, UserUpdate

import uuid

SECRET_KEY = "YOUR_SECRET_KEY"


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


# Настройка стратегии аутентификации JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


jwt_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=jwt_transport,
    get_strategy=get_jwt_strategy,
)


# FastAPI Users
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
