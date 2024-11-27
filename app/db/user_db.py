from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import db_helper
from app.models.user import User


async def get_user_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
