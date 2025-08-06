from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router
from .profiles import router as profiles_router
from .roles import router as roles_router


router = APIRouter(
    prefix='/v1'
)

router.include_router(users_router)
router.include_router(posts_router)
router.include_router(profiles_router)
router.include_router(roles_router)
