import json

from fastapi import Depends, HTTPException, APIRouter
from fastapi.params import Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from auth.dependensies import validate_user, get_current_active_auth_user
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.token import TokenInfo
from core.schemas.user import UserSchema
from auth import utils as auth_utils
from crud.users import get_user_by_username, get_user_by_id

router = APIRouter(
    tags=['JWT'],
    prefix='/jwt'
)








@router.post('/login')
def auth_user_issue_jwt(
        response: Response,
        user: UserSchema = Depends(validate_user),
):
    cart = {}
    jwt_payload = {
        'sub': str(user.id),
        'username': user.username,
        'password': str(user.password),
        'cart': dict(),
        'email': user.email,
        'active': user.active,
    }
    token = auth_utils.encode_jwt(
        payload=jwt_payload,
    )
    response.set_cookie(key='users_access_token', value=token, httponly=True)
    response.set_cookie(key='cart', value=json.dumps(cart), httponly=True, )
    return TokenInfo(
        access_token=token,
    )


@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        'username': user.username,
        'email': user.email,
    }


@router.post('/logout')
async def logout_user(
        response: Response,
):
    response.delete_cookie(key='users_access_token')
    return {
        'message': 'Пользователь успешно вышел из системы',
    }