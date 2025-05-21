from datetime import date
from typing import Annotated

import application.events.usecases as use_cases
from application.auth.usecases import AuthorizeUseCase
from application.organizations.usecases import ReadAllOrganizationUseCase
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.events.dtos import (
    ReadAllEventsFeedDto,
    ReadEventUsersDto,
    ReadUserEventsDto,
)
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.organizations.dtos import ReadOrganizationsDto
from domain.users.entities import User
from fastapi import APIRouter, Depends, Request

import infrastructure.api.v1.events.dtos as dtos
import infrastructure.api.v1.events.mappers as mappers
import infrastructure.api.v1.events.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user
from infrastructure.api.v1.organizations.mappers import (
    map_to_pydantic as map_organization,
)

router = APIRouter(route_class=DishkaRoute, tags=["Events"])


@router.get("/", response_model=list[models.EventModel])
async def read_all_events(
    use_case: FromDishka[use_cases.ReadForFeedEventsUseCase],
    dto: dtos.ReadAllEventsFeedModelDto = Depends(),
):
    return map(
        mappers.map_to_pydantic,
        await use_case(mappers.map_read_all_dto_from_pydantic(dto)),
    )


@router.get("/filters", response_model=models.FilterModel)
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


@router.get(
    "/subscribe/my",
    response_model=list[models.EventUserModel],
)
async def read_my_subscribes(
    use_case: FromDishka[use_cases.ReadForUserEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
    page: int = 0,
    page_size: int = 50,
):
    return map(
        mappers.event_user_map_to_pydantic,
        await use_case(
            ReadUserEventsDto(user_id=actor.id, page=page, page_size=page_size),
            actor,
        ),
    )


@router.get(
    "/subscribe/{event_id}",
    response_model=list[models.EventUserModel],
    responses={404: {"model": ErrorModel}},
)
async def read_subscribers(
    event_id: int,
    use_case: FromDishka[use_cases.ReadForEventEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
    page: int = 0,
    page_size: int = 50,
):
    return map(
        mappers.event_user_map_to_pydantic,
        await use_case(
            ReadEventUsersDto(
                event_id=event_id, page=page, page_size=page_size
            ),
            actor,
        ),
    )


@router.post(
    "/subscribe/{event_id}",
    response_model=models.EventUserModel,
    responses={404: {"model": ErrorModel}},
)
async def subscribe(
    event_id: int,
    use_case: FromDishka[use_cases.CreateEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.event_user_map_to_pydantic(await use_case(event_id, actor))


@router.delete(
    "/subscribe/{event_id}",
    response_model=models.EventUserModel,
    responses={404: {"model": ErrorModel}},
)
async def unsubscribe(
    event_id: int,
    use_case: FromDishka[use_cases.DeleteEventUserUseCase],
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.event_user_map_to_pydantic(await use_case(event_id, actor))


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
    actor: Annotated[User, Depends(get_user)],
):
    return mappers.map_to_pydantic(await use_case(event_id, actor))


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
