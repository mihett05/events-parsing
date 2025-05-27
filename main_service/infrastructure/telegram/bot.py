from aiogram import Bot, Dispatcher
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from .router import router


async def create_bot(container: AsyncContainer) -> tuple[Bot, Dispatcher]:
    """
        Обработчик сообщений о событиях из RabbitMQ.
        """
    telegram_bot = await container.get(Bot)
    dp = Dispatcher()
    dp.include_router(router)
    setup_dishka(container, router=dp, auto_inject=True)
    return telegram_bot, dp
