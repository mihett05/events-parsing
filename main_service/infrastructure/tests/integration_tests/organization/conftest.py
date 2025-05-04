from datetime import datetime
from typing import Callable

import pytest
import pytest_asyncio
from httpx import AsyncClient

from domain.organizations.entities import Organization
from infrastructure.api.v1.organizations.dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)
from infrastructure.api.v1.organizations.models import OrganizationModel
from infrastructure.tests.integration_tests.conftest import random_string_factory


@pytest.fixture
def organization_model_factory() -> Callable[[], OrganizationModel]:
    def _factory(
        id: int = 1,
        title: str = "Test Organization",
        created_at: datetime = datetime.now(),
        owner_id: int = 1,
    ) -> OrganizationModel:
        return OrganizationModel(id=id, title=title, created_at=created_at, ownerId=owner_id)

    return _factory


@pytest.fixture
def create_organization_model_dto_factory(random_string_factory) -> Callable[..., CreateOrganizationModelDto]:
    def _factory(
         title: str = random_string_factory(10), created_at: datetime = datetime.now()
    ) -> CreateOrganizationModelDto:
        return CreateOrganizationModelDto(title=title, createdAt=created_at)

    return _factory


@pytest.fixture
def update_organization_model_dto_factory(random_string_factory) -> Callable[[], UpdateOrganizationModelDto]:
    def _factory(
        title: str = random_string_factory(10),
    ) -> UpdateOrganizationModelDto:
        return UpdateOrganizationModelDto(title=title)

    return _factory

@pytest_asyncio.fixture
async def create_organization_model_dtos(
    create_organization_model_dto_factory: Callable[..., CreateOrganizationModelDto],
    random_string_factory,
) -> list[CreateOrganizationModelDto]:
    dtos = []
    for i in range(10):
        dtos.append(
            create_organization_model_dto_factory(
                title=f"{random_string_factory(10)}",
            )
        )
    return dtos


@pytest_asyncio.fixture
async def generate_organizations(
    create_organization_model_dtos: list[CreateOrganizationModelDto],
    async_client,
    user_with_token_model,
):
    organization_models = []
    headers = {"Authorization": f"Bearer {user_with_token_model.access_token}"}
    for dto in create_organization_model_dtos:
        response = await async_client.post(
            "/v1/organizations/",
            json=dto.model_dump(by_alias=True, mode="json"),
            headers=headers,
        )
        json = response.json()
        organization_models.append(OrganizationModel(**json))
    yield organization_models
    for model in organization_models:
        await async_client.delete(f"/v1/organizations/{model.id}", headers=headers)