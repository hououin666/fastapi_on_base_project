from typing import Sequence, Any, Type

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

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
) -> Type[User] | None:
    stmt = select(User).where(User.id==user_id)
    result = await session.scalars(stmt)
    user = result.one_or_none()
    if user:
        return user
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'user with user_id {user_id} not found!'
    )


async def get_active_users(
        session: AsyncSession,
) -> Sequence[Row[Any] | RowMapping | Any]:
    stmt = select(User).where(User.active == True)
    result = await session.scalars(stmt)
    users = result.all()
    if users:
        return users
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'active users not found!'
    )


async def get_active_user_by_id(
        session: AsyncSession,
        user_id: int,
) -> User:
    stmt = select(User).where(User.id==user_id, User.active==True)
    result = await session.scalars(stmt)
    user = result.one_or_none()
    if user:
        return user
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'active user with user_id {user_id} not found!'
    )
