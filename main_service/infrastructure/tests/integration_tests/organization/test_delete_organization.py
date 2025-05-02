from typing import Callable

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.organizations.dtos import CreateOrganizationModelDto
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_delete_organization_success(
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
    result = OrganizationModel(**response.json())

    response = await async_client.delete(
        f"/v1/organizations/{result.id}",
        headers=headers,
    )
    result = OrganizationModel(**response.json())

    assert response.status_code == HTTP_200_OK
    assert result.title == dto.title

    response = await async_client.get(f"/v1/organizations/{result.id}", headers=headers)
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_organization_not_found(
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
    result = OrganizationModel(**response.json())
    await async_client.delete(
        f"/v1/organizations/{result.id}",
        headers=headers,
    )
    response = await async_client.delete(
        f"/v1/organizations/{result.id}",
        headers=headers,
    )

    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_organization_unauthorized(
        async_client: AsyncClient,
        create_organization_model_dto_factory: Callable[..., CreateOrganizationModelDto]
):
    headers = {"Authorization": "Bearer Bismillahov Bismillah Bismillahovich"}

    response = await async_client.delete(
        "/v1/organizations/228",
        headers=headers,
    )

    assert response.status_code == HTTP_401_UNAUTHORIZED