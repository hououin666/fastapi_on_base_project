from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from crud import posts as posts_crud

router = APIRouter(
    tags=['Posts']
)


@router.get('/posts')
async def get_all_posts(

):
    pass


@router.post('/post')
async def create_post(
        user_id: int,
        title: str,
        body: str,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await posts_crud.create_post(user_id=user_id, title=title, body=body, session=session,)