from datetime import datetime
from typing import Callable

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_401_UNAUTHORIZED, HTTP_200_OK

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.organizations.dtos import CreateOrganizationModelDto
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_create_organization_success(
        async_client: AsyncClient,
        user_with_token_model: UserWithTokenModel,
        create_organization_model_dto_factory: Callable[..., CreateOrganizationModelDto]
):
    user = user_with_token_model
    dto = create_organization_model_dto_factory()
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.post(
        "/v1/organizations/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_200_OK
    result = OrganizationModel(**response.json())
    assert result.title == dto.title

    await async_client.delete(
        f"/v1/organizations/{result.id}",
        headers=headers,
    )

@pytest.mark.asyncio
async def test_create_organization_unprocessable_entity(
        async_client: AsyncClient,
        user_with_token_model: UserWithTokenModel,
        create_organization_model_dto_factory: Callable[..., CreateOrganizationModelDto]
):
    user = user_with_token_model
    dto = create_organization_model_dto_factory()
    dto.title = None
    headers = {"Authorization": f"Bearer {user.access_token}"}
    response = await async_client.post(
        "/v1/organizations/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_create_organization_unauthorized(
    async_client: AsyncClient,
    user_with_token_model: UserWithTokenModel,
    create_organization_model_dto_factory: Callable[..., CreateOrganizationModelDto]
):
    user = user_with_token_model
    dto = create_organization_model_dto_factory()
    dto.title = None
    headers = {"Authorization": f"Bearer Bismillahov Bismillah Bismillahovich"}
    response = await async_client.post(
        "/v1/organizations/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED
