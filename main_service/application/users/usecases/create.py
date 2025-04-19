from domain.users.entities import User
from domain.users.repositories import UsersRepository


class CreateUserUseCase:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository

    async def __call__(self, user: User) -> User:
        return await self.__repository.create(user)
