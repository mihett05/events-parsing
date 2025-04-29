from domain.organizations.entities import Organization
from domain.organizations.repositories import (
    OrganizationsRepository,
)
from domain.users.entities import User

from application.organizations.dtos import UpdateOrganizationDto
from application.transactions import TransactionsGateway


class UpdateOrganizationUseCase:
    def __init__(
        self, repository: OrganizationsRepository, tx: TransactionsGateway
    ):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(
        self, dto: UpdateOrganizationDto, actor: User | None
    ) -> Organization:
        async with self.__transaction:
            organization = await self.__repository.read(dto.id)
            organization.title = dto.title
            return await self.__repository.update(organization)
