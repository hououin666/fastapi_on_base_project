from fastapi import APIRouter
from .api_v1 import router as api_v1_router
from auth.auth_jwt import router as auth_jwt_router

router = APIRouter(prefix='/api')

router.include_router(api_v1_router)
router.include_router(auth_jwt_router)

