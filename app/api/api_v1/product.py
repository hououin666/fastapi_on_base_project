from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependensies import get_current_admin_user
from core.models.db_helper import db_helper
from core.schemas.product import ProductCreate, ProductShow
from core.schemas.user import UserSchema
from crud import product as product_crud

router = APIRouter(
    tags=['Product'],
    prefix='/product'
)


@router.post('/create', response_model=ProductShow)
async def create_product(
        product: ProductCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        user: UserSchema = Depends(get_current_admin_user),
):
    return await product_crud.create_product(product=product,session=session)


@router.post('/add-count', response_model=ProductShow)
async def add_product_count(
        product_id: int,
        count: int,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await product_crud.add_product_count(product_id=product_id, session=session, count=count)


