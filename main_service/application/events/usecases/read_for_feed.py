from domain.events.dtos import ReadAllEventsFeedDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadForFeedEventsUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadAllEventsFeedDto) -> list[Event]:
        return await self.__repository.read_for_feed(dto)
