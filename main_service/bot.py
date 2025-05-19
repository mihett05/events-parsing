import asyncio

from infrastructure.providers.container import create_container
from infrastructure.telegram.bot import create_bot


async def main():
    container = create_container()
    bot, dp = await create_bot(container)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
