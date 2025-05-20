from domain.users.dtos import CreateActivationTokenDto
from domain.users.entities import UserActivationToken
from domain.users.repositories import UserActivationTokenRepository


class CreateUserActivationTokenUseCase:
    def __init__(self, repository: UserActivationTokenRepository):
        self.__repository = repository

    async def __call__(
        self, dto: CreateActivationTokenDto
    ) -> UserActivationToken:
        return await self.__repository.create(dto)
