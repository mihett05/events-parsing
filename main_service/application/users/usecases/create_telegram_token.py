from domain.users.dtos import CreateTelegramTokenDto
from domain.users.entities import User
from domain.users.repositories import TelegramTokensRepository


class CreateTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
    ):
        self.__repository = repository

    async def __call__(self, bot_name: str, actor: User) -> str:
        token = await self.__repository.create(CreateTelegramTokenDto(actor.id))
        return f"t.me/{bot_name}?start={token.id}"
