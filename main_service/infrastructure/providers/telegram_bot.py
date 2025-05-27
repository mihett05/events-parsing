from aiogram import Bot
from dishka import Provider, Scope, provide

from infrastructure.config import Config


class BotProvider(Provider):
    """
    Провайдер для инициализации и управления Telegram ботом.

    Предоставляет экземпляр бота с областью видимости на уровне приложения (APP),
    что означает единственный экземпляр бота на все время работы приложения.
    """

    scope = Scope.APP

    @provide
    async def get_bot(self, config: Config) -> Bot:
        """Создает и возвращает экземпляр Telegram бота."""

        return Bot(token=config.telegram_bot_token)
