import pytest
from application.organizations.usecases import ReadOrganizationUseCase
from domain.organizations.entities import Organization


@pytest.mark.asyncio
async def test_read_organization(
    read_organization_usecase: ReadOrganizationUseCase,
    create_organization: Organization,
):
    return_organization = await read_organization_usecase(
        create_organization.id
    )
    assert return_organization == create_organization
