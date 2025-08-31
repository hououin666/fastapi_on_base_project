import json

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_410_GONE

from auth.dependensies import get_current_token_payload_user, get_current_active_auth_user
from core.models import Product
from core.schemas.user import UserSchema
from crud.product import get_product_by_id


def get_cart_by_user(
        payload: dict,
        request: Request,
):
    cart: dict = dict(payload.get('cart'))
    cart_cookie = request.cookies.get('cart')
    decode_cart_cookie = json.loads(cart_cookie)
    return decode_cart_cookie
    # raise HTTPException(
    #     status_code=HTTP_404_NOT_FOUND,
    #     detail='Корзина не найдена!'
    # )


async def add_product_to_cart(
        product_id: int,
        session: AsyncSession,
        payload: dict,
        request: Request,
        response: Response,
):
    product: Product = await get_product_by_id(product_id=product_id, session=session)
    cart = get_cart_by_user(payload=payload, request=request)
    if product.count >= 1:
        if cart.get(f'{product.name}') is None:
            cart[f'{product.name}'] = 1
        else:
            cart[f'{product.name}'] += 1
        product.count -= 1
    else:
        raise HTTPException(
            status_code=HTTP_410_GONE,
            detail='Товара нет в наличии'
        )
    response.set_cookie(key='cart', value=json.dumps(cart), httponly=True, )
    await session.commit()
    return cart


async def remove_product_from_cart(
        product_id: int,
        session: AsyncSession,
        payload: dict,
        request: Request,
        response: Response,
):
    product: Product = await get_product_by_id(product_id=product_id, session=session)
    cart = get_cart_by_user(payload=payload, request=request)
    if cart.get(f'{product.name}') is not None:
        if cart.get(f'{product.name}') == 1:
            cart.pop(f'{product.name}')
        else:
            cart[f'{product.name}'] -= 1
        product.count += 1
    else:
        raise HTTPException(
            status_code=HTTP_410_GONE,
            detail='Товар отсутствует в корзине'
        )
    response.set_cookie(key='cart', value=json.dumps(cart), httponly=True, )
    await session.commit()
    return cart

