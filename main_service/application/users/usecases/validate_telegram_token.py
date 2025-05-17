from uuid import UUID

from domain.users.entities import User
from domain.users.exceptions import TelegramTokenNotFoundError
from domain.users.repositories import TelegramTokensRepository

from application.users.usecases.read_telegram_token import (
    ReadTelegramTokenUseCase,
)


class ValidateTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
        read_use_case: ReadTelegramTokenUseCase,
    ):
        self.__repository = repository
        self.__read_use_case = read_use_case

    async def __call__(self, token_id: UUID, actor: User) -> bool:
        try:
            token = await self.__read_use_case(token_id, actor)
            return not token.is_used
        except TelegramTokenNotFoundError:
            return False
