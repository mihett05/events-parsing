from domain.events.dtos import ReadUserEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadUserEventsUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadUserEventsDto) -> list[Event]:
        return await self.__repository.read_for_user(dto)
