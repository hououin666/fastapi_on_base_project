from fastapi import Depends, HTTPException, APIRouter
from fastapi.params import Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from core.models import User
from core.models.db_helper import db_helper
from core.schemas.token import TokenInfo
from core.schemas.user import UserSchema
from auth import utils as auth_utils

router = APIRouter(
    tags=['JWT'],
    prefix='/jwt'
)


async def validate_user(
        session: AsyncSession = Depends(db_helper.session_getter),
        username: str = Form(),
        password: str = Form(),
):
    stmt = select(User).where(User.username==username)
    result = await session.scalars(stmt)
    user = result.one_or_none()
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


@router.post('/login')
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_user)
):
    jwt_payload = {
        'sub': user.id,
        'username': user.username,
        'password': str(user.password),
        'email': user.email,
        'active': user.active,
    }
    token = auth_utils.encode_jwt(
        payload=jwt_payload,
    )
    return TokenInfo(
        access_token=token,
        token_type = 'Bearer'
    )