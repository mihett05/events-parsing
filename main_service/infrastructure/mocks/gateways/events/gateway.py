import asyncio

from application.events.coordinator.gateway import CoordinatorGateway
from domain.mails.entities import Mail


class MemoryCoordinatorGateway(CoordinatorGateway):
    async def run(self, mails: list[Mail]):
        await asyncio.sleep(0.1)  # imitation of publishing mails to process
