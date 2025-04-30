from random import randint
from typing import Callable

import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import CreateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel


@pytest.mark.asyncio
async def test_register_success(
    async_client: AsyncClient,
    create_user_model_dto_factory: Callable[..., CreateUserModelDto],
):
    dto = create_user_model_dto_factory(email=f"example{randint(0, 100)}@example.com")
    response = await async_client.post(
        "/v1/auth/register",
        json=dto.model_dump(by_alias=True, mode="json"),
    )

    assert response.status_code == status.HTTP_200_OK
    response_model = UserWithTokenModel(**response.json())

    attrs = ("email", "fullname", "is_active")
    for attr in attrs:
        assert getattr(dto, attr) == getattr(response_model.user, attr)

    response = await async_client.delete(
        "/v1/users/",
        headers={"Authorization": f"Bearer {response_model.access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
