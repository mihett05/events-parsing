from domain.users.entities import User
from domain.users.repositories import UsersRepository


class ReadUsersByIdsUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, user_ids: list[int]) -> list[User]:
        return await self.__repository.read_by_ids(user_ids)
