from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependensies import get_current_admin_user
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.role import RoleCreate
from crud import roles as roles_crud

router = APIRouter(
    tags=['Roles (Admin only)'],
)

@router.get('/roles')
async def get_all_roles(
        session: AsyncSession = Depends(db_helper.session_getter),
        admin: User = Depends(get_current_admin_user)
):
    return await roles_crud.get_all_roles(session=session)


@router.post('/role')
async def create_role(
        role: RoleCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        admin: User = Depends(get_current_admin_user),
):
    return await roles_crud.create_role(role=role, session=session)


@router.delete('/role/{role_id}')
async def delete_role_by_id(
        role_id: int,
        session: AsyncSession = Depends(db_helper.session_getter),
        admin: User = Depends(get_current_admin_user)
):
    return await roles_crud.delete_role_by_id(role_id=role_id, session=session)


@router.post('/role/{user_id}/{role_name}')
async def set_role_to_user_by_id(
        user_id: int,
        role_name: str,
        session: AsyncSession = Depends(db_helper.session_getter),
        admin: User = Depends(get_current_admin_user)
):
    return await roles_crud.set_role_to_user_by_id(user_id=user_id, role_name=role_name, session=session)
