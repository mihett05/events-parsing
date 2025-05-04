from typing import Callable, Coroutine, Any

import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from infrastructure.api.v1.auth.models import UserWithTokenModel
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.mark.asyncio
async def test_update_organization_success(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    update_organization_model_dto_factory,
):
    organization_model = generate_organizations[0]
    dto = update_organization_model_dto_factory()
    user_with_token = await user_with_token_model()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}


    response = await async_client.put(
        f"/v1/organizations/{organization_model.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_200_OK

    response2 = await async_client.get(f"/v1/organizations/{organization_model.id}")
    organization_model = OrganizationModel(**response2.json())

    assert organization_model.title == dto.title


@pytest.mark.asyncio
async def test_update_organization_unauthorized(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
    update_organization_model_dto_factory,
):
    dto = update_organization_model_dto_factory()
    organization_model = generate_organizations[0]
    headers = {"Authorization": f"Bearer Bismillahov Bismillah Bismillahovich"}


    response = await async_client.put(
        f"/v1/organizations/{organization_model.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_organization_not_found(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    update_organization_model_dto_factory,
    create_organization_model_dto_factory,
):
    dto = create_organization_model_dto_factory()
    user_with_token = await user_with_token_model()
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}
    response = await async_client.post(
        "/v1/organizations/",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    result = OrganizationModel(**response.json())

    await async_client.delete(f"/v1/organizations/{result.id}", headers=headers)

    dto = update_organization_model_dto_factory()
    response = await async_client.put(
        f"/v1/organizations/{result.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_event_unprocessable_entity(
    generate_organizations: list[OrganizationModel],
    async_client: AsyncClient,
    user_with_token_model: Callable[..., Coroutine[Any, Any, UserWithTokenModel]],
    update_organization_model_dto_factory,
):
    organization_model = generate_organizations[0]
    dto = update_organization_model_dto_factory()
    user_with_token = await user_with_token_model()
    dto.title = None
    headers = {"Authorization": f"Bearer {user_with_token.access_token}"}


    response = await async_client.put(
        f"/v1/organizations/{organization_model.id}",
        json=dto.model_dump(by_alias=True, mode="json"),
        headers=headers,
    )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
