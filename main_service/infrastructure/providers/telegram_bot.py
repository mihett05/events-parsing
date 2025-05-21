from aiogram import Bot
from dishka import Provider, Scope, provide

from infrastructure.config import Config


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, config: Config) -> Bot:
        return Bot(token=config.telegram_bot_token)
