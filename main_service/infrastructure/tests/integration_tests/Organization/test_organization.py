# -------------------------------------------------------
# ------------------ ORGANIZATIONS ----------------------
# -------------------------------------------------------
from datetime import datetime

import pytest
from httpx import AsyncClient

from infrastructure.api.v1.organizations.dtos import CreateOrganizationModelDto
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_create_organization(
    async_client: AsyncClient, user_with_token_model
):
    user = user_with_token_model
    dto = CreateOrganizationModelDto(title="Test Org", createdAt=datetime.now())
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.post(
        "/v1/organizations/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == 200
    result = OrganizationModel(**response.json())
    assert result.title == dto.title


@pytest.mark.asyncio
async def test_read_organization(
    async_client: AsyncClient, user_with_token_model
):
    user = user_with_token_model
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.get("/v1/organizations/1", headers=headers)
    if response.status_code == 200:
        result = OrganizationModel(**response.json())
        assert result.id == 1
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_organization(
    async_client: AsyncClient,
    user_with_token_model,
    update_organization_model_dto_factory,
):
    user = user_with_token_model
    dto = update_organization_model_dto_factory()
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.put(
        "/v1/organizations/1",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    if response.status_code == 200:
        result = OrganizationModel(**response.json())
        assert result.title == dto.title
    else:
        assert response.status_code == 404
