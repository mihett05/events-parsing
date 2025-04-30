from datetime import datetime

import pytest
from httpx import AsyncClient

from infrastructure.api.v1.organizations.dtos import CreateOrganizationModelDto
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_create_organization(async_client: AsyncClient, user_with_token_model):
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

    response = await async_client.delete(
        f"/v1/organizations/{result.id}",
        headers=headers,
    )
    assert response.status_code == 200