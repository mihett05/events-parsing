from application.transactions import TransactionsGateway
from domain.organizations.entities import Organization
from domain.organizations.repositories import (
    OrganizationsRepository,
)
from domain.users.entities import User


class DeleteOrganizationUseCase:
    def __init__(
        self, repository: OrganizationsRepository, tx: TransactionsGateway
    ):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(
        self, organization_id: int, actor: User | None
    ) -> Organization:
        async with self.__transaction:
            organization = await self.__repository.read(organization_id)
            return await self.__repository.delete(organization)
