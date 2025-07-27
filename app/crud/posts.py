from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post
from crud import users as users_crud


async def create_post(
        user_id: int,
        title: str,
        body: str,
        session: AsyncSession,
):
    user = users_crud.get_user_by_id(user_id=user_id, session=session)
    post = Post(
        user_id=user_id,
        title=title,
        body=body,
    )
    session.add(post),
    await session.commit()
    return post


async def get_user_posts(

):
    pass