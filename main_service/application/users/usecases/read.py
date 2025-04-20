from domain.users.entities import User
from domain.users.repositories import UsersRepository


class ReadUserUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, user_id: int) -> User:
        return await self.__repository.read(user_id)
