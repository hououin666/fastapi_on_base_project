from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from auth.dependensies import get_current_token_payload_user, get_current_active_auth_user
from core.models.db_helper import db_helper
from core.schemas.user import UserSchema
from crud import cart as cart_crud

router = APIRouter(
    tags=['Cart'],
)


@router.get('/user/cart')
def get_cart_by_user(
        request: Request,
        payload = Depends(get_current_token_payload_user),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    return cart_crud.get_cart_by_user(payload=payload, request=request)


@router.post('/user/cart/add')
async def add_product_to_cart():
    pass