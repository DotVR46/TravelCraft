from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from app.db.db_helper import db_helper
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=list[UserRead], description="Получить всех пользователей")
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)
