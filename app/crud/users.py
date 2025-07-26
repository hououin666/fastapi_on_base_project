from typing import Sequence

from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.models.db_helper import db_helper
from core.schemas.user import UserRead, UserCreate


async def get_all_users(
        session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
        session: AsyncSession,
        user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_user_by_id(
        session: AsyncSession,
        user_id: int,
):
    stmt = select(User).where(User.id == user_id)
    result = await session.scalars(stmt)
    return result.all()