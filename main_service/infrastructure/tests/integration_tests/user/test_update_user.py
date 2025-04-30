import pytest
from httpx import AsyncClient

from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient,
    user_with_token_model,
    update_user_model_dto_factory,
):
    user = user_with_token_model
    dto = update_user_model_dto_factory()
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.put(
        f"/v1/users/{user.user.id}",
        json=dto.model_dump(by_alias=True),
        headers=headers,
    )
    assert response.status_code == 200
    result = UserModel(**response.json())
    assert result.fullname == dto.fullname
    assert result.telegram_id == dto.telegram_id
