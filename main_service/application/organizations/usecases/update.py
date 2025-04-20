from main_service.application.organizations.dtos import UpdateOrganizationDto
from main_service.application.transactions import TransactionsGateway
from main_service.domain.organizations.entities import Organization
from main_service.domain.organizations.repositories import (
    OrganizationRepository,
)
from main_service.domain.users.entities import User


class UpdateOrganizationUsecase:
    def __init__(
        self, repository: OrganizationRepository, tx: TransactionsGateway
    ):
        self.__repository = repository
        self.__transaction = tx

    async def __call__(
        self, dto: UpdateOrganizationDto, actor: User
    ) -> Organization:
        async with self.__transaction:
            organization = await self.__repository.read(dto.organization_id)
            organization.title = dto.title
            organization.members = dto.members
            organization.roles = dto.roles
            await self.__repository.update(organization)

        return organization
