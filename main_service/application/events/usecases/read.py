from domain.events.entities import Event

from domain.events.repositories import EventsRepository


class ReadEventUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, event_id: int) -> Event:
        return await self.__repository.read(event_id)
