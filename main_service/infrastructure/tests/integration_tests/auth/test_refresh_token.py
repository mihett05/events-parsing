import pytest
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_refresh_token_success(
        get_test_client: AsyncClient,
        get_authenticate_user1_model_dto: AuthenticateUserModelDto,
        get_user1_model: UserModel,
        create_user1,
):
    response = await get_test_client.post(
        "/v1/auth/login",
        json=get_authenticate_user1_model_dto.model_dump(
            by_alias=True, mode="json"
        ),
    )

    get_test_client.cookies.set("refresh", response.cookies.get("refresh"))
    response2 = await get_test_client.post("/v1/auth/refresh")
    assert response2.status_code == status.HTTP_200_OK

    response_model = UserWithTokenModel(**response2.json())
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
