import pytest
from fastapi.testclient import TestClient

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto
from infrastructure.api.v1.auth.models import UserWithTokenModel


@pytest.mark.asyncio
async def test_register_success(
    get_test_client: TestClient,
    get_create_user_model_dto: AuthenticateUserModelDto,
):
    response = get_test_client.post(
        "/v1/auth/login",
        json=get_create_user_model_dto.model_dump(by_alias=True, mode="json"),
    )
    assert response.status_code == 200
    model = UserWithTokenModel(**response.json())

    assert model.user == {
        "email": "test@test.com",
        "fullname": "Ivanov Ivan Ivanovich",
        "isActive": True,
        "telegramId": None
    }