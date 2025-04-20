from domain.users.dtos import ReadAllUsersDto
from domain.users.entities import User
from domain.users.repositories import UsersRepository


class ReadAllUsersUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, dto: ReadAllUsersDto) -> list[User]:
        return await self.__repository.read_all(dto)
