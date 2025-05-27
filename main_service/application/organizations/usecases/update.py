from domain.organizations.entities import Organization
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User
from domain.users.role_getter import RoleGetter

from application.auth.enums import PermissionsEnum
from application.auth.permissions import PermissionBuilder
from application.organizations.dtos import UpdateOrganizationDto
from application.organizations.permissions import OrganizationPermissionProvider
from application.organizations.usecases.read import ReadOrganizationUseCase
from application.transactions import TransactionsGateway


class UpdateOrganizationUseCase:
    """
    Реализует бизнес-логику обновления данных организации.

    Инкапсулирует процесс изменения информации об организации,
    включая проверку прав доступа и обеспечение целостности данных
    в рамках транзакции.
    """

    def __init__(
        self,
        repository: OrganizationsRepository,
        transaction: TransactionsGateway,
        permission_builder: PermissionBuilder,
        role_getter: RoleGetter,
        read_organization_use_case: ReadOrganizationUseCase,
    ):
        """
        Инициализирует сценарий обновления организации.
        """

        self.__repository = repository
        self.__transaction = transaction
        self.__builder = permission_builder
        self.__role_getter = role_getter
        self.__read_organization_use_case = read_organization_use_case

    async def __call__(self, dto: UpdateOrganizationDto, actor: User) -> Organization:
        """
        Выполняет сценарий обновления организации.
        """

        async with self.__transaction:
            organization = await self.__read_organization_use_case(dto.id)
            actor_role = await self.__role_getter(actor, organization.id)
            self.__builder.providers(
                OrganizationPermissionProvider(actor_role, dto.id)
            ).add(PermissionsEnum.CAN_UPDATE_ORGANIZATION).apply()
            organization.title = dto.title
            return await self.__repository.update(organization)
