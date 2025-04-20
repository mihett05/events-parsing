from fastapi import APIRouter
import application.organizations.usecases as use_cases
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from infrastructure.api.v1.organizations import models
from infrastructure.api.v1.organizations import mappers

from main_service.application.organizations.dtos import UpdateOrganizationDto
from main_service.application.organizations.usecases.read_all import (
    ReadAllOrganizationUsecase,
)
from main_service.domain.organizations.dtos import (
    ReadOrganizationsDto,
    CreateOrganizationDto,
)
from main_service.infrastructure.api.models import ErrorModel

router = APIRouter(route_class=DishkaRoute, tags=["Organizations"])


@router.post(
    "/",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def create_organization(
    dto: CreateOrganizationDto,
    use_case: FromDishka[use_cases.CreateOrganizationUsecase],
):
    return await use_case(mappers.map_create_dto_from_pydantic(dto))


@router.get("/", response_model=list[models.OrganizationModel])
async def read_all_organizations(
    use_case: FromDishka[use_cases.ReadAllOrganizationUsecase],
    page: int = 0,
    page_size: int = 50,
):
    return map(
        lambda organization: mappers.map_to_pydantic(organization),
        await use_case(ReadOrganizationsDto(page=page, page_size=page_size)),
    )


@router.get(
    "/{organization_id}",
    response_model=list[models.OrganizationModel],
    responses={404: {"model": ErrorModel}},
)
async def read_organization(
    organization_id: int,
    use_case: FromDishka[use_cases.ReadOrganizationUsecase],
):
    return mappers.map_to_pydantic(await use_case(organization_id))


@router.put(
    "/{organization_id}",
    response_model=models.OrganizationModel,
    responses={404: {"model": ErrorModel}},
)
async def update_organization(
    organization_id: int,
    dto: UpdateOrganizationDto,
    use_case: FromDishka[use_cases.UpdateOrganizationUsecase],
):
    return mappers.map_to_pydantic(
        await use_case(
            mappers.map_update_dto_from_pydantic(dto, organization_id), None
        )
    )


@router.delete(
    "/{organization_id}",
    response_model=list[models.OrganizationModel],
    responses={404: {"model": ErrorModel}},
)
async def delete_organization(
    organization_id: int,
    use_case: FromDishka[use_cases.DeleteOrganizationUsecase],
):
    return mappers.map_to_pydantic(await use_case(organization_id, None))
