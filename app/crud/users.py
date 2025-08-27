from typing import Sequence, Any, Type

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from core.models import User, Profile
from core.models.db_helper import db_helper
from core.schemas.user import UserRead, UserCreate
from auth import utils as auth_utils


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
    user_in_db = await get_user_by_username(username=user_create.username, session=session)
    if user_in_db:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail='user with this username already exist',
        )
    hash_pw = auth_utils.hashcode_pw(user_create.password)
    user = User(
        username=user_create.username,
        password=hash_pw,
        email=user_create.email,
        active=user_create.active,
    )
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


async def get_user_by_username(
        username: str,
        session: AsyncSession,
) -> User:
    stmt = select(User).where(User.username==username)
    result = await session.scalars(stmt)
    user = result.one_or_none()
    if user:
        return user


async def create_user_profile(
        user_id: int,
        first_name: str,
        last_name: str,
        session: AsyncSession,
):
    try:
        profile = Profile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name
                          )
        session.add(profile)
        await session.commit()
        return profile
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f'profile for user with user_id {user_id} already exists!'
        )



async def get_user_profile_by_id(
        user_id: int,
        session: AsyncSession,
):
    stmt = select(Profile).where(Profile.user_id==user_id)
    result = await session.scalars(stmt)
    profile = result.one_or_none()
    if profile:
        return profile
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'profile with user_id {user_id} not found!'
    )