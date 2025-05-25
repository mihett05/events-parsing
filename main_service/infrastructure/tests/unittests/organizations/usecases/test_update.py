from copy import copy

import pytest
from application.organizations.dtos import UpdateOrganizationDto
from application.organizations.usecases import UpdateOrganizationUseCase
from domain.organizations.entities import Organization
from domain.organizations.exceptions import OrganizationNotFoundError
from domain.users.entities import User


@pytest.mark.asyncio
async def test_update_organization(
    update_organization_usecase: UpdateOrganizationUseCase,
    update_organization_dto: UpdateOrganizationDto,
    get_admin_organization: Organization,
    get_admin: User,
):
    get_admin_organization = copy(get_admin_organization)
    # TODO: change actor to userreturn await self.__repository.read(user_id)
    return_organization = await update_organization_usecase(
        update_organization_dto, get_admin
    )
    assert return_organization.title != get_admin_organization.title
    assert return_organization.title == update_organization_dto.title


@pytest.mark.asyncio
async def test_update_not_found(
    update_organization_usecase: UpdateOrganizationUseCase,
    update_organization_dto: UpdateOrganizationDto,
):
    update_organization_dto.id = 3434
    with pytest.raises(OrganizationNotFoundError):
        # TODO: change actor to user
        _ = await update_organization_usecase(update_organization_dto, None)
