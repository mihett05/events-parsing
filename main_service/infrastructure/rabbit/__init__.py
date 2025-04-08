from faststream.rabbit import RabbitRouter

from .events.router import router as events_router

router = RabbitRouter()
router.include_router(events_router)
