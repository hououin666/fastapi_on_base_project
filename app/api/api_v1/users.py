from typing import Sequence, Any, Type, Coroutine, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from auth.dependensies import get_current_admin_user
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.profile import ProfileUser
from core.schemas.user import UserRead, UserCreate, UserSchema
from crud import users as users_crud

router = APIRouter(
    tags=['Users']
)

@router.get('/users')
async def get_users(
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_admin_user),
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post('/user', response_model=UserRead)
async def create_user(
        user_create: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) :
    user = await users_crud.create_user(session=session, user_create=user_create)
    return user


@router.get('/users/active',)
async def get_active_users(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    users = await users_crud.get_active_users(session=session)
    return users


@router.get('/user/{user_id}', response_model=UserSchema)
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
) -> User:
    user = await users_crud.get_user_by_id(session=session, user_id=user_id)
    return user


@router.get('/user/{user_id}/active', response_model=UserSchema)
async def get_active_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await users_crud.get_active_user_by_id(session=session, user_id=user_id)
    return user


@router.get('/user-by-username/{username}')
async def get_user_by_username(
        username: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    user = await users_crud.get_user_by_username(session=session, username=username)
    if user:
        return user
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'user with username {username} not found!'
    )



