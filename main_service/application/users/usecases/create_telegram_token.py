from aiogram import Bot
from domain.users.dtos import CreateTelegramTokenDto
from domain.users.entities import User
from domain.users.repositories import TelegramTokensRepository


class CreateTelegramTokenUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
        telegram_bot: Bot,
    ):
        self.__repository = repository
        self.__bot = telegram_bot

    async def __call__(self, actor: User) -> str:
        token = await self.__repository.create(CreateTelegramTokenDto(actor.id))
        return f"t.me/{(await self.__bot.get_me()).username}?start={token.id}"
