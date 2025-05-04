import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_read_all_organizations_success(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
):
    page = 0
    page_size = 50
    response = await async_client.get(
        f"/v1/organizations/", params={"page": page, "page_size": page_size}
    )
    assert response.status_code == HTTP_200_OK