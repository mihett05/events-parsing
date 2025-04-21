from fastapi import APIRouter

from .auth import router as auth_router
from .events import router as event_router
from .users import router as user_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(event_router, prefix="/events")
v1_router.include_router(user_router, prefix="/users")
