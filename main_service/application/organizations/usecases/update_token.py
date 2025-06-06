from uuid import UUID

from domain.organizations.entities import OrganizationToken
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User
from domain.users.repositories import UsersRepository
from infrastructure.config import Config

from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway


class UpdateOrganizationTokenUseCase:
    """
    Реализует бизнес-логику активации токена организации.

    Инкапсулирует процесс пометки токена как использованного
    и связывания его с конкретным пользователем,
    обеспечивая атомарность операций через вложенные транзакции.
    """

    def __init__(
        self,
        transaction: TransactionsGateway,
        repository: OrganizationTokensRepository,
        read_use_case: ReadOrganizationTokenUseCase,
        users_repository: UsersRepository,
        config: Config,
    ):
        """
        Инициализирует сценарий обновления токена организации.
        """

        self.__transaction = transaction
        self.__repository = repository
        self.__read_use_case = read_use_case
        self.__users_repository = users_repository
        self.__config = config

    async def __call__(self, token_id: UUID, actor: User) -> OrganizationToken:
        """
        Выполняет сценарий активации токена организации.
        """

        async with self.__transaction.nested():
            super_user = await self.__users_repository.read_by_email(
                self.__config.admin_username
            )
            token = await self.__read_use_case(token_id, super_user)
            token.used_by = actor.id
            token.is_used = True
            return await self.__repository.update(token)
