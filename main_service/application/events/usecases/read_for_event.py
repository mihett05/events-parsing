from domain.events.dtos import ReadEventUsersDto
from domain.events.entities import EventUser
from domain.events.repositories import EventUsersRepository
from domain.users.entities import User


class ReadEventUsersUseCase:
    def __init__(self, repository: EventUsersRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadEventUsersDto, actor: User) -> list[EventUser]:
        return await self.__repository.read_for_event(dto)
