from domain.events.dtos import ReadOrganizationEventsDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository


class ReadOrganizationEventsUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadOrganizationEventsDto) -> list[Event]:
        return await self.__repository.read_for_organization(dto)
