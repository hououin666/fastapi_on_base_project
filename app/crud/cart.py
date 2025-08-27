from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND

from auth.dependensies import get_current_token_payload_user, get_current_active_auth_user
from core.schemas.user import UserSchema


def get_cart_by_user(
        payload: dict,
        request: Request,
):
    cart: dict = dict(payload.get('cart'))
    cart_cookie = request.cookies.get('cart')
    return {
        'cart': cart,
        'cart_cookie': cart_cookie,
            }
    # raise HTTPException(
    #     status_code=HTTP_404_NOT_FOUND,
    #     detail='Корзина не найдена!'
    # )

