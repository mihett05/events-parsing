from fastapi import APIRouter

from .events.router import router as event_router

v1_router = APIRouter()
v1_router.include_router(event_router, prefix="/events")
