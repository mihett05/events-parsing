import pytest
from application.organizations.usecases import CreateOrganizationUseCase
from domain.organizations.dtos import CreateOrganizationDto


@pytest.mark.asyncio
async def test_create_success(
    create_organization_usecase: CreateOrganizationUseCase,
    create_organization_dto: CreateOrganizationDto,
):
    organization = await create_organization_usecase(
        dto=create_organization_dto, actor=None
    )
    attrs = ("title", "created_at", "owner_id")
    for attr in attrs:
        assert getattr(organization, attr) == getattr(create_organization_dto, attr)

    assert organization.id == 1
