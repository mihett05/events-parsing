from uuid import UUID

from domain.users.entities import User
from domain.users.exceptions import UserAccessDenied
from domain.users.repositories import TelegramTokensRepository

from application.transactions import TransactionsGateway
from application.users.dtos import UpdateUserDto
from application.users.usecases.update import UpdateUserUseCase
from application.users.usecases.update_telegram_token import UpdateTelegramTokenUseCase
from application.users.usecases.validate_telegram_token import (
    ValidateTelegramTokenUseCase,
)


class ConnectTelegramUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
        update_token_use_case: UpdateTelegramTokenUseCase,
        update_user_use_case: UpdateUserUseCase,
        validate_use_case: ValidateTelegramTokenUseCase,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__update_user_use_case = update_user_use_case
        self.__update_token_use_case = update_token_use_case
        self.__transaction = transaction
        self.__validate_use_case = validate_use_case

    async def __call__(self, token_id: UUID, telegram_id: int, actor: User):
        async with self.__transaction:
            if not await self.__validate_use_case(token_id, actor):
                raise UserAccessDenied

            await self.__update_user_use_case(
                UpdateUserDto(actor.id, actor.fullname, telegram_id), actor
            )
            await self.__update_token_use_case(token_id, actor)
