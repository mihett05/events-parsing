from uuid import UUID

from domain.organizations.exceptions import OrganizationTokenNotFoundError
from domain.organizations.repositories import OrganizationTokensRepository
from domain.users.entities import User

from application.organizations.usecases.read_token import (
    ReadOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway


class ValidateOrganizationTokenUseCase:
    def __init__(
        self,
        repository: OrganizationTokensRepository,
        transaction: TransactionsGateway,
        read_use_case: ReadOrganizationTokenUseCase,
    ):
        self.__repository = repository
        self.__transaction = transaction
        self.__read_use_case = read_use_case

    async def __call__(self, token_id: UUID, actor: User) -> bool:
        async with self.__transaction:
            try:
                token = await self.__read_use_case(token_id)
                return await self.__repository.validate(token)
            except OrganizationTokenNotFoundError:
                return False
