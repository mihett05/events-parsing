from datetime import datetime
from typing import Callable

import pytest

from infrastructure.api.v1.organizations.dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)
from infrastructure.api.v1.organizations.models import OrganizationModel


@pytest.fixture
def organization_model_factory() -> Callable[[...], OrganizationModel]:
    def _factory(
        id: int = 1,
        title: str = "Test Organization",
        created_at: datetime = datetime.now(),
        owner_id: int = 1,
    ) -> OrganizationModel:
        return OrganizationModel(
            id=id, title=title, created_at=created_at, ownerId=owner_id
        )

    return _factory


@pytest.fixture
def create_organization_model_dto_factory() -> Callable[
    [...], CreateOrganizationModelDto
]:
    def _factory(
        title: str = "New Organization", created_at: datetime = datetime.now()
    ) -> CreateOrganizationModelDto:
        return CreateOrganizationModelDto(title=title, createdAt=created_at)

    return _factory


@pytest.fixture
def update_organization_model_dto_factory() -> Callable[
    [...], UpdateOrganizationModelDto
]:
    def _factory(
        title: str = "Updated Organization Title",
    ) -> UpdateOrganizationModelDto:
        return UpdateOrganizationModelDto(title=title)

    return _factory
