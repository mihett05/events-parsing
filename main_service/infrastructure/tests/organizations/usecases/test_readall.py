import pytest

from application.organizations.usecases import ReadAllOrganizationUseCase
from domain.organizations.dtos import ReadOrganizationsDto
from domain.organizations.entities import Organization


@pytest.mark.asyncio
async def test_readall(
    readall_organization_usecase: ReadAllOrganizationUseCase,
    readall_organizations_dto: ReadOrganizationsDto,
    create_organization: Organization,
):
    organizations = await readall_organization_usecase(
        readall_organizations_dto
    )
    assert len(organizations) == 1
    assert organizations[0] == create_organization
