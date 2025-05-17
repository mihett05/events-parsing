from uuid import UUID

from domain.users.entities import TelegramToken, User
from domain.users.repositories import TelegramTokensRepository

from application.users.usecases.read_telegram_token import (
    ReadTelegramTokenUseCase,
)


class UpdateTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
        read_use_case: ReadTelegramTokenUseCase,
    ):
        self.__repository = repository
        self.__read_use_case = read_use_case

    async def __call__(self, token_id: UUID, actor: User) -> TelegramToken:
        token = await self.__read_use_case(token_id, actor)
        token.is_used = True
        return await self.__repository.update(token)
