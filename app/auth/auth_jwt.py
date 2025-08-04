from fastapi import Depends, HTTPException, APIRouter
from fastapi.params import Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from core.models import User
from core.models.db_helper import db_helper
from core.schemas.token import TokenInfo
from core.schemas.user import UserSchema
from auth import utils as auth_utils

router = APIRouter(
    tags=['JWT'],
    prefix='/jwt'
)


http_bearer = HTTPBearer()


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
        'sub': str(user.id),
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


def get_current_token_payload_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    token = credentials.credentials
    payload = auth_utils.decode_jwt(token)
    return payload


async def get_current_auth_user(
        payload = Depends(get_current_token_payload_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    stmt = select(User).where(User.id==int(payload.get('sub')))
    result = await session.scalars(stmt)
    user = result.one_or_none()
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



@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        'username': user.username,
        'email': user.email,
    }