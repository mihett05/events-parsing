from domain.users.entities import User, UserActivationToken
from domain.users.repositories import ActivationTokenRepository


class CreateUserActivationTokenUseCase:
    def __init__(self, repository: ActivationTokenRepository):
        self.__repository = repository

    async def __call__(self, user: User) -> UserActivationToken:
        return await self.__repository.create_activation_token(user)
