from domain.events.entities import Event
from domain.events.repositories import EventsRepository

from application.events.dtos import EventInfo


class FindEventUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: EventInfo) -> Event | None:
        return await self.__repository.find(dto)
