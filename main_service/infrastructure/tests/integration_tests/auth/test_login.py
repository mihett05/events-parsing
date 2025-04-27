import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from starlette import status

from infrastructure.api.v1.auth.dtos import AuthenticateUserModelDto


@pytest.mark.asyncio
async def test_login_success(
    get_test_client: AsyncClient,
    get_authenticate_user1_model_dto: AuthenticateUserModelDto,
    create_user1
):
    response = await get_test_client.post(
        "/v1/auth/login",
        json=get_authenticate_user1_model_dto.model_dump(
            by_alias=True, mode="json"
        ),
    )
    assert response.status_code == status.HTTP_200_OK
