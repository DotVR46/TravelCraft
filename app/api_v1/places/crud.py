from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.place import Place


async def get_products(session: AsyncSession) -> list[Place]:
    stmt = select(Place).order_by(Place.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Place | None:
    return await session.get(Place, product_id)
