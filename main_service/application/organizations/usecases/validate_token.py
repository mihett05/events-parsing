from uuid import UUID

from domain.organizations.exceptions import OrganizationTokenNotFoundError
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User
from domain.users.repositories import UsersRepository
from infrastructure.config import Config

from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway


class ValidateOrganizationTokenUseCase:
    """
    Реализует бизнес-логику валидации токена организации.

    Обеспечивает проверку токена на возможность использования,
    включая проверку его существования и статуса активности.
    """

    def __init__(
        self,
        transaction: TransactionsGateway,
        repository: OrganizationTokensRepository,
        read_use_case: ReadOrganizationTokenUseCase,
        users_repository: UsersRepository,
    ):
        """
        Инициализирует сценарий валидации токена.
        """

        self.__transaction = transaction
        self.__repository = repository
        self.__read_use_case = read_use_case
        self.__users_repository = users_repository

    async def __call__(self, token_id: UUID, actor: User) -> bool:
        """
        Выполняет проверку валидности токена организации.
        """

        async with self.__transaction.nested():
            try:
                super_user = await self.__users_repository.get_super_user()
                token = await self.__read_use_case(token_id, super_user)
                return not token.is_used
            except OrganizationTokenNotFoundError:
                return False
