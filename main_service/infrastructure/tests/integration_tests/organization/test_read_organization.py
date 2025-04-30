import pytest
from httpx import AsyncClient

from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_read_organization(async_client: AsyncClient, user_with_token_model):
    user = user_with_token_model
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.get("/v1/organizations/1", headers=headers)
    if response.status_code == 200:
        result = OrganizationModel(**response.json())
        assert result.id == 1
    else:
        assert response.status_code == 404