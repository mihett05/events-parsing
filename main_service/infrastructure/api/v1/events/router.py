from typing import Annotated

import application.events.usecases as use_cases
from application.organizations.usecases import ReadAllOrganizationUseCase
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.organizations.dtos import ReadOrganizationsDto
from domain.users.entities import User
from fastapi import APIRouter, Depends

import infrastructure.api.v1.events.dtos as dtos
import infrastructure.api.v1.events.mappers as mappers
import infrastructure.api.v1.events.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user
from infrastructure.api.v1.organizations.mappers import (
    map_to_pydantic as map_organization,
)

router = APIRouter(route_class=DishkaRoute, tags=["Events"])


@router.get("/calendar", response_model=list[models.EventModel])
async def read_calendar_events(
    use_case: FromDishka[use_cases.ReadAllEventUseCase],
    dto: dtos.ReadAllEventsCalendarModelDto = Depends(),
):
    return map(
        mappers.map_to_pydantic,
        await use_case(mappers.map_read_all_dto_calendar_from_pydantic(dto)),
    )


@router.get("/feed", response_model=list[models.EventModel])
async def read_feed_events(
    use_case: FromDishka[use_cases.ReadForFeedEventsUseCase],
    dto: dtos.ReadAllEventsFeedModelDto = Depends(),
):
    return map(
        mappers.map_to_pydantic,
        await use_case(mappers.map_read_all_dto_from_pydantic(dto)),
    )


@router.get("/feed_filters", response_model=models.FilterModel)
async def get_filter_values(
    use_case: FromDishka[ReadAllOrganizationUseCase],
):
    return models.FilterModel(
        type=list(map(lambda x: x.value, EventTypeEnum)),
        format=list(map(lambda x: x.value, EventFormatEnum)),
        organization=list(
            map(
                map_organization,
                await use_case(ReadOrganizationsDto(page=None, page_size=None)),
            )
        ),
    )


@router.post(
    "/",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def create_event(
    dto: dtos.CreateEventModelDto,
    use_case: FromDishka[use_cases.CreateEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(
        await use_case(mappers.map_create_dto_from_pydantic(dto), actor)
    )


@router.get(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def read_event(
    event_id: int,
    use_case: FromDishka[use_cases.ReadEventUseCase],
):
    return mappers.map_to_pydantic(await use_case(event_id))


@router.put(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def update_event(
    event_id: int,
    dto: dtos.UpdateEventModelDto,
    use_case: FromDishka[use_cases.UpdateEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(
        await use_case(
            mappers.map_update_dto_from_pydantic(dto, event_id), actor
        )
    )


@router.delete(
    "/{event_id}",
    response_model=models.EventModel,
    responses={404: {"model": ErrorModel}},
)
async def delete_event(
    event_id: int,
    use_case: FromDishka[use_cases.DeleteEventUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(await use_case(event_id, actor))
