from uuid import UUID

import application.users.usecases as use_cases
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka

router = Router()


@router.message(CommandStart())
async def start(
    message: Message,
    use_case: FromDishka[use_cases.ConnectTelegramUseCase],
):
    token = UUID(message.text.split()[1])
    try:
        await use_case(token, message.from_user.id)
        await message.answer("Телеграм успешно обновлен")
    except:
        await message.answer("Произошла ошибка")
