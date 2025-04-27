import pytest
from application.organizations.usecases import (
    DeleteOrganizationUseCase,
    ReadOrganizationUseCase,
)
from domain.organizations.entities import Organization
from domain.organizations.exceptions import OrganizationNotFoundError


@pytest.mark.asyncio
async def test_delete(
    delete_organization_usecase: DeleteOrganizationUseCase,
    read_organization_usecase: ReadOrganizationUseCase,
    create_organization: Organization,
):
    return_organization = await delete_organization_usecase(
        create_organization.id, None
    )
    assert return_organization == create_organization
    with pytest.raises(OrganizationNotFoundError):
        await read_organization_usecase(create_organization.id)
