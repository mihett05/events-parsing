from fastapi import APIRouter

from .attachments import router as attachments_router
from .auth import router as auth_router
from .events import router as event_router
from .organizations import router as organizations_router
from .users import router as user_router

v1_router = APIRouter()
v1_router.include_router(attachments_router, prefix="/attachments")
v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(event_router, prefix="/events")
v1_router.include_router(user_router, prefix="/users")
v1_router.include_router(organizations_router, prefix="/organizations")
