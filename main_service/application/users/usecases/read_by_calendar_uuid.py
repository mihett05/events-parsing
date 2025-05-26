from uuid import UUID

from domain.users.entities import User
from domain.users.repositories import UsersRepository


class ReadByCalendarUUIDUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, uuid: UUID) -> User:
        return await self.__repository.read_by_calendar_uuid(uuid)
