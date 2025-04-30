from datetime import date
from typing import Annotated

import application.events.usecases as use_cases
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from domain.events.dtos import ReadAllEventsDto, ReadAllEventsFeedDto
from domain.events.enums import EventFormatEnum, EventTypeEnum
from domain.users.entities import User
from fastapi import APIRouter, Depends

import infrastructure.api.v1.events.dtos as dtos
import infrastructure.api.v1.events.mappers as mappers
import infrastructure.api.v1.events.models as models
from infrastructure.api.models import ErrorModel
from infrastructure.api.v1.auth.deps import get_user

router = APIRouter(route_class=DishkaRoute, tags=["Events"])


@router.get("/calendar", response_model=list[models.EventModel])
async def read_all_events(
    use_case: FromDishka[use_cases.ReadAllEventUseCase],
    start_date: date | None = None,
    end_date: date | None = None,
):
    return map(
        mappers.map_to_pydantic,
        await use_case(
            ReadAllEventsDto(
                start_date=start_date,
                end_date=end_date,
            )
        ),
    )


@router.get("/feed", response_model=list[models.EventModel])
async def read_all_events(
    use_case: FromDishka[use_cases.ReadForFeedEventsUseCase],
    page: int = 0,
    page_size: int = 50,
    start_date: date | None = None,
    end_date: date | None = None,
    organization_id: int | None = None,
    type_: EventTypeEnum | None = None,
    format_: EventFormatEnum | None = None,
):
    return map(
        mappers.map_to_pydantic,
        await use_case(
            ReadAllEventsFeedDto(
                page=page,
                page_size=page_size,
                start_date=start_date,
                end_date=end_date,
                organization_id=organization_id,
                type=type_,
                format=format_,
            )
        ),
    )


@router.get("/feed_filters")
async def get_types_and_formats() -> dict[str, list]:
    result = dict()
    result["type"] = list(map(lambda x: x.value, EventTypeEnum))
    result["format"] = list(map(lambda x: x.value, EventFormatEnum))
    return result


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
