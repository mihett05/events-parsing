from domain.organizations.dtos import CreateOrganizationDto
from domain.organizations.entities import Organization
from domain.organizations.exceptions import OrganizationAccessDenied
from domain.organizations.repositories import OrganizationsRepository
from domain.users.entities import User

from application.organizations.usecases.validate_token import (
    ValidateOrganizationTokenUseCase,
)


class CreateOrganizationUseCase:
    def __init__(
        self,
        repository: OrganizationsRepository,
        validate_token_use_case: ValidateOrganizationTokenUseCase,
    ):
        self.__repository = repository
        self.__validate_token_use_case = validate_token_use_case

    async def __call__(
        self, dto: CreateOrganizationDto, actor: User
    ) -> Organization:
        if self.__validate_token_use_case(dto.token, actor):
            return await self.__repository.create(dto)
        raise OrganizationAccessDenied
