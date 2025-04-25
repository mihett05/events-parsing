from copy import copy
from venv import create

import pytest

from application.organizations.dtos import UpdateOrganizationDto
from application.organizations.usecases import UpdateOrganizationUseCase
from domain.organizations.entities import Organization


@pytest.mark.asyncio
async def test_update(
    update_organization_usecase: UpdateOrganizationUseCase,
    update_organization_dto: UpdateOrganizationDto,
    create_organization: Organization,
):
    create_organization = copy(create_organization)
    return_organization = await update_organization_usecase(
        update_organization_dto, None
    )
    assert return_organization.title != create_organization.title
    assert return_organization.title == update_organization_dto.title
