import pytest
from fastapi.testclient import TestClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.users.models import UserModel


@pytest.mark.asyncio
async def test_register_success(
        get_test_client: TestClient,
        get_user_model: UserModel,
        get_create_user_model_dto: AuthenticateUserModelDto,
):
    response = get_test_client.post(
        "/v1/auth/register",
        json=get_create_user_model_dto.model_dump(by_alias=True, mode="json"),
    )

    assert response.status_code == 200

    response_model = UserWithTokenModel(**response.json())
    attrs = (
        "email",
        "fullname",
        "is_active",
        "telegram_id",
    )
    for attr in attrs:
        assert getattr(get_user_model, attr) == getattr(response_model.user, attr)

    response_delete_user = get_test_client.delete(
        "/v1/users",
        headers={'Authorization': f'Bearer {response_model.access_token}'},
    )
    assert response_delete_user.status_code == status.HTTP_200_OK
