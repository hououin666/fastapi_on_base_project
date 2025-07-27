from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

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


async def get_all_posts(
    session: AsyncSession,
):
    stmt = select(Post).order_by(Post.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_posts_by_user_id(
        user_id: int,
        session: AsyncSession,
):
    stmt = select(Post).where(Post.user_id == user_id)
    result = await session.scalars(stmt)
    posts = result.all()
    if posts:
        return posts
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f'posts by user with user_id {user_id} not found!'
    )