import pytest
from application.organizations.usecases import ReadAllOrganizationUseCase
from domain.organizations.dtos import ReadOrganizationsDto
from domain.organizations.entities import Organization


@pytest.mark.asyncio
async def test_readall(
    readall_organization_usecase: ReadAllOrganizationUseCase,
    readall_organizations_dto: ReadOrganizationsDto,
    get_admin_organization: Organization,
):
    organizations = await readall_organization_usecase(readall_organizations_dto)
    assert len(organizations) == 1
    assert organizations[0] == get_admin_organization


@pytest.mark.asyncio
async def test_read_all_empty(
    readall_organization_usecase: ReadAllOrganizationUseCase,
    readall_organizations_dto: ReadOrganizationsDto,
):
    readall_organizations_dto.page = 100
    organizations = await readall_organization_usecase(readall_organizations_dto)

    assert len(organizations) == 0
