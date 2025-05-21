from uuid import UUID

from domain.users.entities import TelegramToken
from domain.users.repositories import TelegramTokensRepository


class ReadTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
    ):
        self.__repository = repository

    async def __call__(self, token_id: UUID) -> TelegramToken:
        return await self.__repository.read(token_id)
