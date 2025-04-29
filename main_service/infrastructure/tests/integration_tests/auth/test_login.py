import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_login_success(
    async_client: AsyncClient,
    get_authenticate_user1_model_dto: AuthenticateUserModelDto,
    get_user1_model: UserModel,
    create_user1,
):
    response = await async_client.post(
        "/v1/auth/login",
        json=get_authenticate_user1_model_dto.model_dump(
            by_alias=True, mode="json"
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    response_model = UserWithTokenModel(**response.json())
    attrs = (
        "email",
        "fullname",
        "is_active",
        "telegram_id",
    )
    for attr in attrs:
        assert getattr(get_user1_model, attr) == getattr(
            response_model.user, attr
        )
