from typing import Annotated
from uuid import UUID

import application.organizations.usecases as use_cases
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.organizations.dtos import ReadOrganizationsDto
from domain.users.entities import User
from fastapi import APIRouter, Depends

from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user
from infrastructure.api.v1.organizations import mappers, models
from infrastructure.api.v1.organizations.dtos import (
    CreateOrganizationModelDto,
    UpdateOrganizationModelDto,
)

router = APIRouter(route_class=DishkaRoute, tags=["Organizations"])


@router.post(
    "/",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def create_organization(
    dto: CreateOrganizationModelDto,
    use_case: FromDishka[use_cases.CreateOrganizationUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return await use_case(
        mappers.map_create_dto_from_pydantic(dto, actor), actor
    )


@router.get("/", response_model=list[models.OrganizationModel])
async def read_all_organizations(
    use_case: FromDishka[use_cases.ReadAllOrganizationUseCase],
    page: int | None = None,
    page_size: int | None = None,
):
    return map(
        mappers.map_to_pydantic,
        await use_case(ReadOrganizationsDto(page=page, page_size=page_size)),
    )


@router.get(
    "/{organization_id}",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def read_organization(
    organization_id: int,
    use_case: FromDishka[use_cases.ReadOrganizationUseCase],
):
    return mappers.map_to_pydantic(await use_case(organization_id))


@router.put(
    "/{organization_id}",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def update_organization(
    organization_id: int,
    dto: UpdateOrganizationModelDto,
    use_case: FromDishka[use_cases.UpdateOrganizationUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(
        await use_case(
            mappers.map_update_dto_from_pydantic(dto, organization_id), actor
        )
    )


@router.delete(
    "/{organization_id}",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_organization(
    organization_id: int,
    use_case: FromDishka[use_cases.DeleteOrganizationUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(await use_case(organization_id, actor))


@router.post(
    "/token",
    response_model=models.OrganizationTokenModel,
)
async def create_token(
    use_case: FromDishka[use_cases.CreateOrganizationTokenUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.organization_token_map_to_pydantic(await use_case(actor))


@router.get(
    "/token/{token_id}",
    response_model=models.OrganizationTokenModel,
    responses={404: {"model": ErrorModel}},
)
async def read_token(
    token_id: UUID,
    use_case: FromDishka[use_cases.ReadOrganizationTokenUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.organization_token_map_to_pydantic(
        await use_case(token_id, actor)
    )


@router.delete(
    "/token/{token_id}",
    response_model=models.OrganizationTokenModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_token(
    token_id: UUID,
    use_case: FromDishka[use_cases.DeleteOrganizationTokenUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.organization_token_map_to_pydantic(
        await use_case(token_id, actor)
    )
