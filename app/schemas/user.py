from uuid import UUID

from fastapi_users import schemas



class UserRead(schemas.BaseUser[UUID]):
    first_name: str | None
    last_name: str | None


class UserCreate(schemas.BaseUserCreate):
    first_name: str | None
    last_name: str | None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None
    last_name: str | None
