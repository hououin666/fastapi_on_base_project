from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from core.models.product import Product
from core.schemas.product import ProductCreate
from core.schemas.user import UserSchema


async def create_product(
        product: ProductCreate,
        session: AsyncSession,
):
    new_product = Product(
        name=product.name,
        count=product.count
    )
    session.add(new_product)
    await session.commit()
    return new_product


async def get_product_by_id(
        product_id: int,
        session: AsyncSession,
) -> Product:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    product: Product = result.one_or_none()
    if product:
        return product
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'Продукт с айди {product_id} не найден'
    )


async def add_product_count(
        product_id: int,
        session: AsyncSession,
        count: int,
):
    product: Product = await get_product_by_id(product_id, session)
    product.count += count
    await session.commit()
    return product