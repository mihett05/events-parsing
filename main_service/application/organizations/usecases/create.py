from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.exceptions import OrganizationAccessDenied
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User, UserOrganizationRole
from domain.users.enums import RoleEnum

from application.organizations.usecases.update_token import (
    UpdateOrganizationTokenUseCase,
)
from application.organizations.usecases.validate_token import (
    ValidateOrganizationTokenUseCase,
)
from application.transactions import TransactionsGateway
from application.users.usecases import CreateUserRoleUseCase


class CreateOrganizationUseCase:
    def __init__(
        self,
        repository: OrganizationsRepository,
        validate_token_use_case: ValidateOrganizationTokenUseCase,
        update_token_use_case: UpdateOrganizationTokenUseCase,
        create_use_case: CreateUserRoleUseCase,
        transaction: TransactionsGateway,
    ):
        self.__repository = repository
        self.__validate_token_use_case = validate_token_use_case
        self.__update_token_use_case = update_token_use_case
        self.__create_use_case = create_use_case
        self.__transaction = transaction

    async def __call__(
        self, dto: CreateOrganizationDto, actor: User
    ) -> Organization:
        async with self.__transaction:
            if not await self.__validate_token_use_case(dto.token, actor):
                raise OrganizationAccessDenied

            await self.__update_token_use_case(dto.token, actor)
            organization = await self.__repository.create(dto)
            role = UserOrganizationRole(
                organization_id=organization.id,
                user_id=actor.id,
                role=RoleEnum.OWNER,
            )
            await self.__create_use_case(role, actor)
            return organization
