from fastapi import HTTPException
from fastapi.params import Depends, Form
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from auth import utils as auth_utils
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.user import UserSchema
from crud.roles import get_role_by_name
from crud.users import get_user_by_username, get_user_by_id


async def validate_user(
        session: AsyncSession = Depends(db_helper.session_getter),
        username: str = Form(),
        password: str = Form(),
):
    user = await get_user_by_username(username=username, session=session,)
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='invalid username or password!'
        )
    if auth_utils.validate_passwords(password, user.password):
        return user
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='invalid username or password!'
    )


def get_current_token_payload_user(
    request: Request,
) -> dict:
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='token not found',
        )
    try:
        payload = auth_utils.decode_jwt(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='token has expired'
        )
    return payload


async def get_current_auth_user(
        payload = Depends(get_current_token_payload_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get_user_by_id(user_id=int(payload.get('sub')), session=session)
    if user:
        return user
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='invalid token'
    )


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        HTTP_403_FORBIDDEN,
        detail='user is not active'
    )


async def get_current_admin_user(
        current_user: User = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    admin_role = await get_role_by_name(role_name='Admin', session=session)
    if current_user.role_id == admin_role.id:
        return current_user
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail='Недостаточно прав!',
    )



