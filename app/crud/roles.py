from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from core.models import Role
from core.schemas.role import RoleCreate
from crud.users import get_user_by_id


async def get_all_roles(
        session: AsyncSession,
):
    stmt = select(Role).order_by(Role.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_role_by_id(
        role_id: int,
        session: AsyncSession,
):
    stmt = select(Role).where(Role.id==role_id)
    result = await session.scalars(stmt)
    role = result.one_or_none()
    if role:
        return role
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'role with id {role_id} not found',
    )


async def get_role_by_name(
        role_name: str,
        session: AsyncSession,
):
    stmt = select(Role).where(Role.name == role_name)
    result = await session.scalars(stmt)
    role = result.one_or_none()
    return role



async def create_role(
        role: RoleCreate,
        session: AsyncSession,
):
    exist_role = await get_role_by_name(role_name=role.name, session=session)
    if exist_role:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail='this role already exist',
        )
    new_role = Role(
        name=role.name,
    )
    session.add(new_role)
    await session.commit()
    return new_role


async def delete_role_by_id(
        role_id: int,
        session: AsyncSession,
):
    role = await get_role_by_id(role_id=role_id, session=session)
    await session.delete(role)
    await session.commit()
    return role


async def set_role_to_user_by_id(
        user_id: int,
        role_name: str,
        session: AsyncSession,
):
    role = await get_role_by_name(role_name=role_name, session=session)
    user = await get_user_by_id(user_id=user_id, session=session)
    user.role_id = role.id
    session.add(user)
    await session.commit()
    return user