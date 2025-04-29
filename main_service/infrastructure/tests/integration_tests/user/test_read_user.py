import pytest
from httpx import AsyncClient

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel
from infrastructure.tests.integration_tests.user.conftest import create_user1


@pytest.mark.asyncio
async def test_read_user_success(
    create_user1: UserWithTokenModel,
    get_user1_model: UserModel,
    async_client: AsyncClient,
):
    response = await async_client.get(f"/v1/users/{create_user1.user.id}")
    assert response.status_code == 200
    response_model = UserModel(**response.json())
    attrs = (
        "email",
        "fullname",
        "is_active",
        "telegram_id",
    )
    for attr in attrs:
        assert getattr(get_user1_model, attr) == getattr(response_model, attr)
