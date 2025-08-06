from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.schemas.profile import ProfileUser
from crud import users as users_crud

router = APIRouter(
    tags=['Profiles'],
)



@router.post('/user/create-profile/{user_id}', response_model=ProfileUser)
async def create_user_profile(
        user_id: int,
        first_name: str,
        last_name: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await users_crud.create_user_profile(session=session, user_id=user_id, first_name=first_name, last_name=last_name)


@router.get('/user/profile/{user_id}', response_model=ProfileUser)
async def get_user_profile_by_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await users_crud.get_user_profile_by_id(session=session,user_id=user_id)
