import pytest
from fastapi.testclient import TestClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto


@pytest.mark.asyncio
async def test_login_success(
    get_test_client: TestClient,
    get_authenticate_user_model_dto: AuthenticateUserModelDto,
):
    response = get_test_client.post(
        "/v1/auth/login",
        json=get_authenticate_user_model_dto.model_dump(
            by_alias=True, mode="json"
        ),
    )
    assert response.status_code == status.HTTP_200_OK
