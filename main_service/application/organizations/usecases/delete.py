from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.permissions import OrganizationPermissionProvider
from application.organizations.usecases.read import ReadOrganizationUseCase
from application.transactions import TransactionsGateway
from application.users.usecases import ReadUserRolesUseCase


class DeleteOrganizationUseCase:
    def __init__(
        self,
        repository: OrganizationsRepository,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
        read_roles_use_case: ReadUserRolesUseCase,
        read_organization_use_case: ReadOrganizationUseCase,
    ):
        self.__repository = repository
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__read_roles_use_case = read_roles_use_case
        self.__read_organization_use_case = read_organization_use_case

    async def __call__(self, organization_id: int, actor: User) -> Organization:
        async with self.__transaction:
            organization = await self.__read_organization_use_case(
                organization_id
            )
            roles = await self.__read_roles_use_case(actor.id)
            self.__builder.providers(
                OrganizationPermissionProvider(roles, organization_id)
            ).add(PermissionsEnum.CAN_DELETE_ORGANIZATION).apply()
            return await self.__repository.delete(organization)
