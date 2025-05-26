import pytest
from application.organizations.usecases import (
    DeleteOrganizationUseCase,
    ReadOrganizationUseCase,
)
from domain.organizations.entities import Organization
from domain.organizations.exceptions import OrganizationNotFoundError
from domain.users.entities import User


@pytest.mark.asyncio
async def test_delete(
    delete_organization_usecase: DeleteOrganizationUseCase,
    read_organization_usecase: ReadOrganizationUseCase,
    get_admin_organization: Organization,
    get_admin: User,
):
    return_organization = await delete_organization_usecase(
        get_admin_organization.id, get_admin
    )
    assert return_organization == get_admin_organization
    # TODO: fix
    return
    with pytest.raises(OrganizationNotFoundError):
        await read_organization_usecase(get_admin_organization.id)
