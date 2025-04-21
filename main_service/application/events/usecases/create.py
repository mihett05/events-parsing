from domain.events.dtos import CreateEventDto
from domain.events.entities import Event
from domain.events.repositories import EventsRepository
from domain.users.entities import User


class CreateEventUseCase:
    def __init__(self, repository: EventsRepository):
        self.__repository = repository

    async def __call__(self, dto: CreateEventDto, actor: User | None) -> Event:
        return await self.__repository.create(dto)
