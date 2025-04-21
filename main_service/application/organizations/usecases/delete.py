from main_service.application.transactions import TransactionsGateway
from main_service.domain.organizations.entities import Organization
from main_service.domain.organizations.repositories import (
    OrganizationRepository,
)
from main_service.domain.users.entities import User


class DeleteOrganizationUseCase:
    def __init__(
        self, repository: OrganizationRepository, tx: TransactionsGateway
    ):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(
        self, organization_id: int, actor: User | None
    ) -> Organization:
        async with self.__transaction:
            organization = await self.__repository.read(organization_id)
            await self.__repository.delete(organization)
        return organization
