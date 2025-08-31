from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from auth.dependensies import get_current_token_payload_user, get_current_active_auth_user
from core.models.db_helper import db_helper
from core.schemas.user import UserSchema
from crud import cart as cart_crud

router = APIRouter(
    tags=['Cart'],
)


@router.get('/user/cart/')
def get_cart_by_user(
        request: Request,
        payload = Depends(get_current_token_payload_user),
        user: UserSchema = Depends(get_current_active_auth_user),
):
   cart = cart_crud.get_cart_by_user(payload=payload, request=request)
   return {
       'cart': cart,
   }


@router.post('/user/cart/add')
async def add_product_to_cart(
        request: Request,
        response: Response,
        product_id: int,
        payload = Depends(get_current_token_payload_user),
        user: UserSchema = Depends(get_current_active_auth_user),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await cart_crud.add_product_to_cart(
        product_id=product_id,
        request=request, response=response,
        payload=payload,
        session=session,
    )


@router.post('/user/cart/delete')
async def remove_product_from_cart(
        product_id: int,
        request: Request,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_getter),
        payload: dict = Depends(get_current_token_payload_user),
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return await cart_crud.remove_product_from_cart(
        product_id=product_id,
        request=request,
        response=response,
        session=session,
        payload=payload,
    )

