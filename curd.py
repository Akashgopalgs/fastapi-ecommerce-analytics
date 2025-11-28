from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database_models import Product


async def create_product(db: AsyncSession, product_data: dict):
    db_product = Product(**product_data)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()