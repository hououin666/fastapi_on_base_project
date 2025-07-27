from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.schemas.post import PostUser
from crud import posts as posts_crud

router = APIRouter(
    tags=['Posts']
)


@router.get('/posts')
async def get_all_posts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await posts_crud.get_all_posts(session=session)


@router.post('/post', response_model=PostUser)
async def create_post(
        user_id: int,
        title: str,
        body: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await posts_crud.create_post(user_id=user_id, title=title, body=body, session=session,)


@router.get('/posts/{user_id}')
async def get_user_posts_by_user_id(
        user_id: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await posts_crud.get_user_posts_by_user_id(session=session, user_id=user_id)