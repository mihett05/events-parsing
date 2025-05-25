import pytest
from application.organizations.usecases import CreateOrganizationUseCase
from domain.organizations.dtos import CreateOrganizationDto


@pytest.mark.asyncio
async def test_create_success(
    create_organization_usecase: CreateOrganizationUseCase,
    create_organization_dto: CreateOrganizationDto,
    create_organization_token_usecase,
    get_admin,
):
    org_token = await create_organization_token_usecase(get_admin)
    create_organization_dto.token = org_token.id

    organization = await create_organization_usecase(
        dto=create_organization_dto, actor=get_admin
    )
    attrs = ("title", "owner_id")
    for attr in attrs:
        assert getattr(organization, attr) == getattr(create_organization_dto, attr)
