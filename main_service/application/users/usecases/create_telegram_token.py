from domain.users.dtos import CreateTelegramTokenDto
from domain.users.entities import TelegramToken, User
from domain.users.repositories import TelegramTokensRepository


class CreateTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
    ):
        self.__repository = repository

    async def __call__(self, actor: User) -> TelegramToken:
        return await self.__repository.create(CreateTelegramTokenDto(actor.id))
