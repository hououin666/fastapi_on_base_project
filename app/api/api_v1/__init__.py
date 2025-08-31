from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router
from .profiles import router as profiles_router
from .roles import router as roles_router
from .cart import router as cart_router
from .product import router as product_router


router = APIRouter(
    prefix='/v1'
)

router.include_router(users_router)
router.include_router(posts_router)
router.include_router(profiles_router)
router.include_router(roles_router)
router.include_router(cart_router)
router.include_router(product_router)
