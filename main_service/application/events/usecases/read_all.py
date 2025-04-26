from domain.events.dtos import ReadAllEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadAllEventUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadAllEventsDto) -> list[Event]:
        return await self.__repository.read_all(dto)
