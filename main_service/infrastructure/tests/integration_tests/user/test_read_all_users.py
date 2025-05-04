import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_read_all_users_success(async_client: AsyncClient, create_users):
    page = 0
    page_size = 50
    response = await async_client.get(f"/v1/users/", params={"page": page, "page_size": page_size})
    assert response.status_code == HTTP_200_OK
