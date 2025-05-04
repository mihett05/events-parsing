import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_read_organization_success(
        generate_organizations: list[OrganizationModel],
        async_client: AsyncClient,
):
    for model in generate_organizations:
        response = await async_client.get(f"/v1/organizations/{model.id}")
        assert response.status_code == HTTP_200_OK
        assert response.json() == model.model_dump(by_alias=True, mode="json")


@pytest.mark.asyncio
async def test_read_organization_not_found(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
):
    model = generate_organizations[-1]
    response = await async_client.get(f"/v1/organizations/{model.id + 1}")
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_read_organization_unprocessable_entity(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
):
    response = await async_client.get(f"/v1/organizations/bismillah")
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY