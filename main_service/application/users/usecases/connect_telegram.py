from uuid import UUID

from domain.users.entities import User
from domain.users.exceptions import TelegramTokenNotFoundError, UserAccessDenied
from domain.users.repositories import TelegramTokensRepository, UsersRepository
from infrastructure.config import Config

from application.users.dtos import UpdateUserDto
from application.users.usecases.read_telegram_token import (
    ReadTelegramTokenUseCase,
)
from application.users.usecases.update import UpdateUserUseCase


class ConnectTelegramUseCase:
    def __init__(
        self,
        repository: TelegramTokensRepository,
        read_token_use_case: ReadTelegramTokenUseCase,
        update_user_use_case: UpdateUserUseCase,
        users_repository: UsersRepository,
        config: Config,
    ):
        self.__repository = repository
        self.__update_user_use_case = update_user_use_case
        self.__read_token_use_case = read_token_use_case
        self.__users_repository = users_repository
        self.__config = config

    async def __call__(self, token_id: UUID, telegram_id: int):
        try:
            token = await self.__read_token_use_case(token_id)
        except TelegramTokenNotFoundError:
            raise UserAccessDenied
        super_user = await self.__users_repository.read_by_email(
            self.__config.admin_username
        )
        await self.__update_user_use_case(
            UpdateUserDto(user_id=token.user_id, telegram_id=telegram_id),
            super_user,
        )
        token.is_used = True
        await self.__repository.update(token)
